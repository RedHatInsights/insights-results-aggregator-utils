#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2021 Red Hat, Inc
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

"""Script to simulate user actions done on OCM UI through the standard REST API.

Description
-----

This script can be used to simulate user actions available on OCM UI related
with recommendations. It interacts with the external data pipeline on Stage
environment.

For a given organization and cluster, the tool allows to simulate the
following operations:
- vote for a rule
- enable a rule
- disable a rule
- disable a rule then enable it

REST API on Stage environment is accessed through proxy. Proxy name should be
provided via CLI together with user name and password used for basic auth.

Usage
-----

``` usage: ui_actions.py [-h] -a ADDRESS [-x PROXY] [-u USER] [-p PASSWORD] -c CLUSTER [-l
CLUSTER_LIST_FILE] [-r RECOMMENDATION] [-e OPERATION [OPERATION ...]] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Address of REST API for external data pipeline
  -x PROXY, --proxy PROXY
                        Proxy to be used to access REST API
  -u USER, --user USER  User name for basic authentication
  -p PASSWORD, --password PASSWORD
                        Password for basic authentication
  -c CLUSTER_UUID, --cluster CLUSTER_UUID
                        UUID of the cluster to interact with
  -l FILE, --cluster-list FILE
                        File containing list of clusters to interact with
                        (1 or more cluster uuid expected)
  -s SELECTOR, --rule-selector SELECTOR
                        Recommendation we want to operate upon (PLUGIN|EK format)
  -e OPERATION [OPERATION ...], --execute OPERATION [OPERATION ...]
                        Operation(s) to perform on the provided recommendation.
                        Accepted operations are:
                          - "like"
                          - "dislike"
                          - "reset_vote"
                          - "enable"
                          - "disable"
                          - "disable_with_feedback"
    -v, --verbose       Make execution more verbose

Notes:

- The following arguments need to be specified:
  -a, --address
  -s, --rule-selector
  -e, --execute
  EITHER -c, --cluster OR -l, --cluster-list

- The file provided to --cluster-list should contain space and/or
linebreak separated UUIDs.

- The --execute argument accepts multiple operations, that would be
executed sequentially in the given order
```

Examples
-----

* Thumbs up vote for a given recommendation

``` ui_actions.py -a 'https://$REST_API_URL' -c '$CLUSTER_ID' -v \
-s 'some.valid.module|ERROR_KEY' -e like -u '$USER' \
-p '$PASSWORD' ```

* Disable a given recommendation

``` ui_actions.py -a 'https://$REST_API_URL' -c '$CLUSTER_ID' -v \
-s 'some.valid.module|ERROR_KEY' -e disable -u '$USER' -p '$PASSWORD' ```


* Disable a given recommendation with feedback

``` ui_actions.py -a 'https://$REST_API_URL' -c '$CLUSTER_ID' -v |
-s 'some.valid.module|ERROR_KEY' -e disable_with_feedback "some feedback" \
-u '$USER' -p '$PASSWORD' ```

* Execute multiple actions for a given recommendation

``` ui_actions.py -a 'https://$REST_API_URL' -c '$CLUSTER_ID' -v \
-s 'some.valid.module|ERROR_KEY' -e disable_with_feedback 'some feedback' \
enable dislike -u '$USER' -p '$PASSWORD' ```

``` ui_actions.py -a 'https://$REST_API_URL' -c '$CLUSTER_ID' -v \
-s 'some.valid.module|ERROR_KEY' -e disable_with_feedback enable \
dislike -u '$USER' -p '$PASSWORD' ```

Note: disable_with_feedback expects a feedback message (string),
and if none is provided, no feedback is sent.

Generated documentation in literate programming style
-----
<https://redhatinsights.github.io/insights-results-aggregator-utils/packages/ui_actions.html>
"""

from argparse import ArgumentParser
import requests

import re
import sys

ALLOWED_OPERATIONS = {
    "like",
    "dislike",
    "reset_vote",
    "enable",
    "disable",
    "disable_with_feedback"
}

REGISTERED_OPERATIONS = []


def register_operation(op, arg=None):
    REGISTERED_OPERATIONS.append(
        [op, arg]
    )


def cli_arguments():
    """Retrieve all CLI arguments provided by user."""
    parser = ArgumentParser()

    parser.add_argument("-a", "--address", dest="address", required=True,
                        help="Address of REST API for external data pipeline")

    parser.add_argument("-x", "--proxy", dest="proxy", required=False,
                        help="Proxy to be used to access REST API")

    parser.add_argument("-u", "--user", dest="user", required=False,
                        help="User name for basic authentication")

    parser.add_argument("-p", "--password", dest="password", required=False,
                        help="Password for basic authentication")

    parser.add_argument("-o", "--organization", dest="organization",
                        help="ID of the organization to interact with")

    parser.add_argument("-c", "--cluster", dest="cluster",
                        required=not ({'-l', '--cluster-list'} & set(sys.argv)),
                        help="UUID of the cluster to interact with")

    parser.add_argument("-l", "--cluster-list", dest="cluster_list_file",
                        required=not ({'-c', '--cluster'} & set(sys.argv)),
                        help="File containing list of clusters to interact with\
                            (1 or more cluster uuid expected)")

    parser.add_argument("-s", "--rule-selector", dest="selector",
                        help="Recommendation we want to operate upon (PLUGIN|EK format)")

    help_message_execute_op = """Operation(s) to perform on the provided recommendation.
    Accepted operations are:
      - "like"
      - "dislike"
      - "reset_vote"
      - "enable"
      - "disable"
      - "disable_with_feedback"
    """
    parser.add_argument("-e", "--execute", dest="operations", action='append', nargs='+',
                        help=help_message_execute_op, required=True)

    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=None,
                        help="Make messages verbose", required=False)

    return parser.parse_args()


def check_api_response(response):
    assert response is not None, "Proper response expected"
    assert response.status_code == requests.codes.ok, \
        "Received {response.status_code} when {requests.codes.ok} expected "


def print_url(url, rest_op, data):
    print("\t", f"Operation: {rest_op}", url, f"{data}" if data else "")


def execute_operations(address, proxies, auth, clusters, plugin, error_key):
    for cluster in clusters:
        for item in REGISTERED_OPERATIONS:
            op = item[0]
            url = f"{address}clusters/{cluster}/rules/{plugin}.report/error_key/{error_key}/{op}"
            print_url(url, "PUT", None)
            if op == "like":
                check_api_response(requests.put(
                    url, proxies=proxies, auth=auth))
            elif op == "dislike":
                check_api_response(requests.put(
                    url, proxies=proxies, auth=auth))
            elif op == "reset_vote":
                check_api_response(requests.put(
                    url, proxies=proxies, auth=auth))
            elif op == "enable":
                check_api_response(requests.put(
                    url, proxies=proxies, auth=auth))
            elif op == "disable":
                check_api_response(requests.put(
                    url, proxies=proxies, auth=auth))
                if item[1]:
                    url = f"{address}/clusters/{cluster}/rules/{plugin}.report/" \
                          f"error_key/{error_key}/disable_feedback"
                    feedback_message = {"message": item[1]}
                    print_url(url, "POST", feedback_message)
                    check_api_response(requests.post(
                        url, proxies=proxies, auth=auth, json=feedback_message))


def main():
    """Entry point to this script."""
    # Parse and process and command line arguments.
    args = cli_arguments()

    # check -c and -l args are not both provided
    if args.cluster and args.cluster_list_file:
        print(f"{sys.argv[0]}: "
              f"error: Please provide cluster UUID through either -c or -l, not both.")
        sys.exit(1)

    # validate the recommendation to work with
    selector = args.selector
    """
    Match any string that has alphanumeric characters separated by at least one dot
    (".") before a vertical line ("|"), followed by only uppercase characters,
    numbers, or underscores ("_")
    """
    if not re.match(r'[a-zA-Z_0-9]+\.[a-zA-Z_0-9.]+\|[A-Z_0-9]+$', selector):
        print(f"{sys.argv[0]}: error: Please provide a valid rule selector (plugin|ek)")
        sys.exit(1)

    # validate operation(s) to execute
    operations = args.operations[0]
    for idx, op in enumerate(operations):
        if op not in ALLOWED_OPERATIONS:
            # Only OK if it is the feedback for disable_with_feedback
            if not (type(op) == str and operations[idx - 1] == "disable_with_feedback"):
                print(f"{sys.argv[0]}: error: Received operation: {op}.")
                print(f"{sys.argv[0]}: error: Expected one of {ALLOWED_OPERATIONS}.")
                print(f"{sys.argv[0]}: error: Please provide a valid operation.")
                sys.exit(1)
        elif op == "disable_with_feedback":
            if len(operations) == 1 or \
                    idx + 1 == len(operations) or \
                    operations[idx + 1] in ALLOWED_OPERATIONS:
                # disable_with_feedback provided without feedback
                print(f"{sys.argv[0]}: warning: {op} without feedback string")
                register_operation("disable")
            else:
                register_operation("disable", operations[idx + 1])
        else:
            register_operation(op)

    verbose = args.verbose
    proxies = {
        'https': args.proxy
    } if args.proxy else None
    auth = (args.user, args.password)
    clusters = {args.cluster} if args.cluster else set(open(args.cluster_list_file).read().split())
    plugin = selector.split("|")[0]
    error_key = selector.split("|")[1]

    if verbose:
        print("Proxy settings:", proxies)
        print("Auth settings:", auth)
        print("Address:", args.address)
        print("Cluster(s):", clusters)
        print("Rule selector:", selector)
        print("Plugin:", plugin)
        print("Error Key:", error_key)
        print("Operations:", REGISTERED_OPERATIONS)

    execute_operations(args.address, proxies, auth, clusters, plugin, error_key)


# If this script is started from command line, run the `main` function which is
# entry point to the processing.
if __name__ == "__main__":
    main()
