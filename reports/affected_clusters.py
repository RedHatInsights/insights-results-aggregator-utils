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

"""
Prints all clusters that are affected by selected rule.

This script can be used to analyze data exported from `report` table by
the following command typed into PSQL console:

    \copy report to 'reports.csv' csv

Script displays two tables:
    1. org_id + cluster_name (list of affected clusters)
    2. org_id + number of affected clusters (usually the only information reguired by management)

Howto connect to PSQL console:
    psql -h host

Password can be retrieved from OpenShift console, for example from:
ccx-data-pipeline-qa/browse/secrets/ccx-data-pipeline-db
ccx-data-pipeline-prod/browse/secrets/ccx-data-pipeline-db
"""

import json
import sys
import csv
import collections

# Check if both command line arguments are specified (they are mandatory).
if len(sys.argv) < 3:
    print("Usage:")
    print("  affected_clusters.py rule_name input_file.csv")
    print("Example:")
    print("  affected_clusters.py ccx_rules_ocp.external.bug_rules.bug_12345678.report report.csv")
    sys.exit(1)

# First command line argument should contain rule name.
rule_name = sys.argv[1]

# Second command line argument should contain name of input CSV.
input_csv = sys.argv[2]

orgs = collections.Counter()

# Try to open the CSV file specified.
with open(input_csv) as csv_input:
    # And open this file as CSV
    csv_reader = csv.reader(csv_input)
    print("Organization", "Cluster name", sep=",")

    # Read all rows from the provided CSV file.
    for row in csv_reader:
        org_id = row[0]
        cluster_id = row[1]
        raw_report = row[2]

        # Try to load JSON file with name found in the CSV file.
        data = json.loads(raw_report)

        # Content of JSON file is a bit complicated, but we need to process
        # only several attributes.
        if "info" in data:
            infolist = data["info"]
            cluster = None
            for info in infolist:
                if info["key"] == "GRAFANA_LINK":
                    cluster = info["details"]["cluster_id"]
            if cluster is not None:
                if "pass" in data:
                    passed = data["pass"]
                    for p in passed:
                        rule = p["component"]
                        if rule == rule_name:
                            print("passed", org_id, cluster_id)
                if "skips" in data:
                    skipped = data["skips"]
                    for s in skipped:
                        rule = s["rule_fqdn"]
                        if rule == rule_name:
                            pass
                            # not important for this report ATM
                            # print("skipped")
                if "reports" in data:
                    reports = data["reports"]
                    for r in reports:
                        rule = r["component"]
                        if rule == rule_name:
                            print(org_id, ',"'+cluster_id+'"', sep="")
                            orgs[org_id] += 1

# Start the processing.
print("Organization", "Clusters affected", sep=",")
sum = 0

# Process all organizations.
for org in orgs:
    print(org, orgs[org], sep=",")
    sum += orgs[org]

# Display total number of organizations.
print("Total=", sum)
