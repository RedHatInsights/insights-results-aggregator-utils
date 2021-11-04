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

This script can be used to retrieve list of clusters from the external data
pipeline through the standard REST API. Organization ID (a.k.a. account number)
needs to be provided via CLI option, because list of clusters is filtered by
organization.

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
                        Organization ID/account number
  -l, --cluster-list    Operation to retrieve list of clusters via REST API
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
    """Retrieve all CLI arguments."""
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
                        help="Organization ID/account number")

    parser.add_argument("-l", "--cluster-list", dest="cluster_list", action="store_true",
                        help="Operation to retrieve list of clusters via REST API",
                        default=None)

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


def retrieve_cluster_list(organization, address, proxies, auth, verbose):
    """Retrieve list of clusters from the external data pipeline REST API endpoint."""
    # construct URL to get list of clusters for given organization ID/account number
    url = '{}/v1/organizations/{}/clusters'.format(address, organization)

    if verbose:
        print("URL to access:", url)

    # send request to REST API
    response = requests.get(url, proxies=proxies, auth=auth)

    # elementary check for response content
    assert response is not None, "Proper response expected"
    assert response.status_code == 200, "Unexpected HTTP code returned: {}".format(
            response.status_code)

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


# If this script is started from command line, run the `main` function which is
# entry point to the processing.
if __name__ == "__main__":
    main()
