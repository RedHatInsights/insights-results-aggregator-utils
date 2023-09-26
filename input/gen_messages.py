#!/usr/bin/env python3

# Copyright © 2022 Red Hat, Inc.
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

"""
Generates messages to be consumed by Insights Results Aggregator.

This script read input message (that should be correct or incorrect, according
to needs) and generates bunch of new messages derived from input one. Each
generated message can be updated if needed - Org ID can changed, cluster ID can
changed as well etc.

Types of possible input message modification:
    * Org ID (if enabled by CLI flag -g)
    * Account number (if enabled by CLI flag -a)
    * Cluster ID (if enabled by CLI flag -c)

It is also possible to specify pattern for output message filenames. For example:
generated_message_{}.json


usage: gen_messages.py [-h] [-i INPUT] [-o OUTPUT] [-r REPEAT] [-g] [-a] [-c] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Specification of input file
  -o OUTPUT, -output OUTPUT
                        Specification of pattern of output file names
  -r REPEAT, --repeat REPEAT
                        Number of generated files
  -g, --org-id          Enable organization ID modification
  -a, --account-number  Enable account number modification
  -c, --cluster-id      Enable cluster ID modification
  -v, --verbose         Make messages verbose
"""

# Link to generated documentation for this script:
# <https://redhatinsights.github.io/insights-results-aggregator-utils/packages/gen_messages.html>

import json
import random
import uuid

from argparse import ArgumentParser
from tqdm import tqdm

# ranges for attributes that can be modified
MIN_ORG_ID = 0
MAX_ORG_ID = 100000000

MIN_ACCOUNT_NUMBER = 0
MAX_ACCOUNT_NUMBER = 100000000


def cli_arguments():
    """Retrieve all CLI arguments provided by user."""

    # First of all, we need to specify all command line flags that are
    # recognized by this tool.
    parser = ArgumentParser()

    # All supported command line arguments and flags
    parser.add_argument(
        "-i",
        "--input",
        dest="input",
        default="input.json",
        required=False,
        help="Specification of input file",
    )

    parser.add_argument(
        "-o",
        "-output",
        dest="output",
        default="output_{}.json",
        required=False,
        help="Specification of pattern of output file names",
    )

    parser.add_argument(
        "-r",
        "--repeat",
        dest="repeat",
        type=int,
        default=10,
        required=False,
        help="Number of generated files",
    )

    parser.add_argument(
        "-g",
        "--org-id",
        dest="org_id",
        action="store_true",
        help="Enable organization ID modification",
        default=None,
    )

    parser.add_argument(
        "-a",
        "--account-number",
        dest="account_number",
        action="store_true",
        help="Enable account number modification",
        default=None,
    )

    parser.add_argument(
        "-c",
        "--cluster-id",
        dest="cluster_id",
        action="store_true",
        help="Enable cluster ID modification",
        default=None,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=None,
        help="Make messages verbose",
        required=False,
    )

    # Now it is time to parse flags, check the actual content of command line
    # and fill-in the object named `args`.
    return parser.parse_args()


def load_json(filename):
    """Load and decode JSON file."""
    with open(filename) as fin:
        return json.load(fin)


def generate_output(filename, payload, verbose=False):
    """Generate output JSON file with indentation."""
    with open(filename, "w") as f:
        json.dump(payload, f, indent=4)
        if verbose:
            print("Generated file {}".format(filename))


def modify_org_id(payload):
    """Change the attribute with organization ID."""
    payload["OrgID"] = random.randint(MIN_ORG_ID, MAX_ORG_ID)


def modify_account_number(payload):
    """Change the attribute account number."""
    payload["AccountNumber"] = random.randint(MIN_ACCOUNT_NUMBER, MAX_ACCOUNT_NUMBER)


def modify_cluster_id(payload):
    """Change the attribute with cluster ID."""
    payload["ClusterName"] = str(uuid.uuid4())


def main():
    """Entry point to this script."""

    # First of all, we need to parse all command line flags that are
    # recognized by this tool.
    args = cli_arguments()
    print(args.input)

    # Read input message
    payload = load_json(args.input)

    # Generate specified number of output messages
    for i in tqdm(range(args.repeat)):

        # optional modifications
        if args.org_id:
            modify_org_id(payload)

        if args.account_number:
            modify_account_number(payload)

        if args.cluster_id:
            modify_cluster_id(payload)

        output_filename = args.output.format(i)
        generate_output(output_filename, payload, args.verbose)


# If this script is started from command line, run the `main` function which is
# entry point to the processing.
if __name__ == "__main__":
    main()
