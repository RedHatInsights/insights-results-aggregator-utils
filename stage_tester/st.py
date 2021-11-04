#!/usr/bin/env python3

# Copyright © 2021 Pavel Tisnovsky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script to retrieve results from the external data pipeline through the standard REST API.

Description
-----

This script can be used to perform several operations with external data
pipeline usually deployed on Stage environment.

First operation retrieves list of clusters from the external data pipeline
through the standard REST API. Organization ID needs to be provided via CLI
option, because list of clusters is filtered by organization.

Second operation retrieves results from the external data pipeline for several
clusters. List of clusters needs to be stored in a text file. Name of this text
file is to be provided by `-i` command line option.

REST API on Stage environment is accessed through proxy. Proxy name should be
provided via CLI together with user name and password used for basic auth.

Usage
-----

```
st.py [-h] -a ADDRESS -r PROXY -u USER -p PASSWORD -o ORGANIZATION [-l] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Address of REST API for external data pipeline
  -x PROXY, --proxy PROXY
                        Proxy to be used to access REST API
  -u USER, --user USER  User name for basic authentication
  -p PASSWORD, --password PASSWORD
                        Password for basic authentication
  -o ORGANIZATION, --organization ORGANIZATION
                        Organization ID
  -l, --cluster-list    Operation to retrieve list of clusters via REST API
  -r, --retrieve-results
                        Retrieve results for given list of clusters via REST
                        API
  -i INPUT, --input INPUT
                        Specification of input file (with list of clusters,
                        for example)
  -v, --verbose         Make messages verbose
```

Generated documentation
-----
<https://redhatinsights.github.io/insights-results-aggregator-utils/packages/st.html>
"""


import requests
import json

from argparse import ArgumentParser


def cli_arguments():
    """Retrieve all CLI arguments provided by user."""
    # First of all, we need to specify all command line flags that are
    # recognized by this tool.
    parser = ArgumentParser()

    # All supported command line arguments and flags
    parser.add_argument("-a", "--address", dest="address", required=True,
                        help="Address of REST API for external data pipeline")

    parser.add_argument("-x", "--proxy", dest="proxy", required=True,
                        help="Proxy to be used to access REST API")

    parser.add_argument("-u", "--user", dest="user", required=True,
                        help="User name for basic authentication")

    parser.add_argument("-p", "--password", dest="password", required=True,
                        help="Password for basic authentication")

    parser.add_argument("-o", "--organization", dest="organization", required=True,
                        help="Organization ID")

    parser.add_argument("-l", "--cluster-list", dest="cluster_list", action="store_true",
                        help="Operation to retrieve list of clusters via REST API",
                        default=None)

    parser.add_argument("-r", "--retrieve-results", dest="retrieve_results", action="store_true",
                        help="Retrieve results for given list of clusters via REST API",
                        default=None)

    parser.add_argument("-i", "--input", dest="input", default=None, required=False,
                        help="Specification of input file (with list of clusters, for example)")

    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=None,
                        help="Make messages verbose")

    # Now it is time to parse flags, check the actual content of command line
    # and fill in the object named `args`.
    return parser.parse_args()


def main():
    """Entry point to this script."""
    # Parse and process and command line arguments.
    args = cli_arguments()
    verbose = args.verbose

    # setup proxy or proxies
    proxies = {
       'https': args.proxy
    }

    if verbose:
        print("Proxy settings:", proxies)

    # tuple with items needed to be filled for basic authentication
    auth = (args.user, args.password)

    if verbose:
        print("Auth settings:", auth)

    if args.cluster_list:
        retrieve_cluster_list(args.organization, args.address, proxies, auth, verbose)

    if args.retrieve_results:
        retrieve_results(args.address, proxies, auth, args.input, verbose)


def retrieve_cluster_list(organization, address, proxies, auth, verbose):
    """Retrieve list of clusters from the external data pipeline REST API endpoint."""
    # construct URL to get list of clusters for given organization ID
    url = f'{address}/v1/organizations/{organization}/clusters'

    if verbose:
        print("URL to access:", url)

    # send request to REST API
    response = requests.get(url, proxies=proxies, auth=auth)

    # elementary check for response content
    assert response is not None, "Proper response expected"
    assert response.status_code == requests.codes.ok, \
        f"Unexpected HTTP code returned: {response.status_code}"

    # response should be in JSON format, time to parse it
    payload = response.json()
    assert payload is not None, "JSON response expected"

    # check the payload content
    assert "status" in payload, "'status' field needs to be present in the payload"
    assert "clusters" in payload, "'clusters' field needs to be present in the payload"

    # print list of clusters to standard output
    clusters = sorted(payload["clusters"])
    for cluster in clusters:
        print(cluster)


def retrieve_results(address, proxies, auth, input_file, verbose):
    """Retrieve results from the external data pipeline REST API endpoint."""
    errors = {}

    # input file containing list of clusters
    with open(input_file, "r") as input_file:
        # iterate over all cluster names
        for line in input_file:
            cluster = line.strip()

            if verbose:
                print("Cluster: ", cluster)

            # construct URL to get report for one specified cluster
            url = f'{address}/v1/clusters/{cluster}/report'

            if verbose:
                print("URL to access:", url)

            try:
                # try to retrieve results for given cluster
                retrieve_results_for_cluster(url, proxies, auth, cluster, verbose)
            except Exception as e:
                # store error to be used later
                errors[cluster] = e

    display_errors(errors)


def display_errors(errors):
    """Display all errors or exceptions thrown during the selected operation."""
    print("-"*60)

    if len(errors) > 0:
        print("Errors detected during results processing")
        for cluster, e in errors.items():
            print(cluster, repr(e))
    else:
        print("No errors found")

    print("-"*60)


def retrieve_results_for_cluster(url, proxies, auth, cluster, verbose):
    """Retrieve results for one specified cluster and store it into the file."""
    # send request to REST API
    response = requests.get(url, proxies=proxies, auth=auth)

    # elementary check for response content
    assert response is not None, "Proper response expected"
    assert response.status_code == requests.codes.ok, \
        f"Unexpected HTTP code returned: {response.status_code}"

    # response should be in JSON format, time to parse it
    payload = response.json()
    assert payload is not None, "JSON response expected"

    # check the payload content
    assert "status" in payload, "'status' field needs to be present in the payload"

    # pretty print the output
    results = json.dumps(payload, indent=4)

    filename = "{}.json".format(cluster)

    # generate output file with cluster results
    with open(filename, "w") as json_file:
        json_file.write(results)


# If this script is started from command line, run the `main` function which is
# entry point to the processing.
if __name__ == "__main__":
    main()
