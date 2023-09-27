#!/usr/bin/env python3

# Copyright © 2020 Red Hat, Inc.
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

"""Converts outputs from OCP rule engine into proper reports.

All input files that have filename 's_*.json' (usually anonymized
outputs from OCP rule engine') are converted into proper 'report'
that can be:

    1. Published into Kafka topic
    2. Stored directly into aggregator database

It is done by inserting organization ID, clusterName and lastChecked
attributes and by rearranging output structure. Output files will
have following names: 'r_*.json'.
"""

# Link to generated documentation for this script:
# <https://redhatinsights.github.io/insights-results-aggregator-utils/packages/2report.html>

import json
import sys
import datetime
from os import listdir
from os.path import isfile, join

# Retrieve list of files in current directory.
files = [f for f in listdir(".") if isfile(join(".", f))]

# Check if both command line arguments are specified (they are mandatory).
if len(sys.argv) < 3:
    print("Usage: 2report.py org_id cluster_id")

# First command line argument should contain organization ID.
orgID = sys.argv[1]

# Second command line argument should contain cluster name.
clusterName = sys.argv[2]

# Retrieve actual time and format it according to ISO standard.
lastChecked = datetime.datetime.utcnow().isoformat() + "Z"


def remove_internal_rules(data, key, selector):
    """Filter all rules and remove internal ones."""
    # Proper JSON reports from OCP should contain attribute named `reports`.
    # It is needed to retrieve its content which is list of reports and
    # process each report separately.
    if "reports" in data:
        if key in data:
            reports = data[key]
            new = []
            for report in reports:
                # Filter out all internal rules.
                if not report[selector].startswith("ccx_rules_ocp.internal."):
                    print("adding", report[selector])
                    new.append(report)
            data[key] = new


# Iterate over all files found in current directory.
for filename in files:
    # Just proper JSON files needs to be processed.
    if filename.startswith("s_") and filename.endswith(".json"):
        # Try to open the given file, read its content, parse it as JSON and
        # use the processed payload later
        with open(filename) as fin:
            data = json.load(fin)
            # Report consists of three - reported problems, passed rules
            # (without problems), and skipped rules. We need to filter out
            # results from internal rules, but interesting is, that `rule_name`
            # is stored under different keys - `component` or `rule_fqdn`. So
            # the madness begins...
            remove_internal_rules(data, "reports", "component")
            remove_internal_rules(data, "pass", "component")
            remove_internal_rules(data, "skips", "rule_fqdn")  # oh my...

            # Construct name of output file
            outfilename = "r_" + filename[2:]

            # Perform the anonymization - the new data structure `report` will
            # contain the original data, but organization ID, cluster ID, and
            # last checked attributes will be changed accordingly
            report = {}
            report["OrgID"] = int(orgID)
            report["ClusterName"] = clusterName
            report["LastChecked"] = lastChecked
            report["Report"] = data

            # Export the anonymized report
            with open(outfilename, "w") as fout:
                json.dump(report, fout, indent=4)
