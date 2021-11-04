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
List all rules and other interesting informations found in reports.csv.

This script can be used to analyze data exported from `report` table by
the following command typed into PSQL console:

    \\copy report to 'reports.csv' csv

Howto connect to PSQL console:
    psql -h host

Password can be retrieved from OpenShift console, for example from:
ccx-data-pipeline-qa/browse/secrets/ccx-data-pipeline-db
ccx-data-pipeline-prod/browse/secrets/ccx-data-pipeline-db
"""

# Link to generated documentation for this script:
# <https://redhatinsights.github.io/insights-results-aggregator-utils/packages/reports.html>

import json
import sys
import csv
import collections

# not supported unless we get the real organization list
import organizations

MOST_USED_ORGS = 50

# Check if command line argument is specified (it is mandatory).
if len(sys.argv) < 2:
    print("Usage:")
    print("  reports.py input_file.csv")
    print("Example:")
    print("  reports.py report.csv")
    sys.exit(1)

# First command line argument should contain name of input CSV.
input_csv = sys.argv[1]

# This variable represents counters for all organizations. Each counter
# contains number of clusters found in the respected organization.
orgs = collections.Counter()

# This variable represents counters for all clusters. Each counter contains
# number of records for this cluster. It should be 1, unless we have some
# problem in database.
clusters = collections.Counter()

# This variable represents counters for all organizations. Each counter contain
# number of clusters hit by any rule.
clusters_hits = collections.Counter()

# This variable represents counters for all organizations. Each counter contain
# number of clusters hit by any rule excluding the tutorial one.
clusters_hits_no_tutorial = collections.Counter()

# This variable represents counters for all rules. Each counter contain number
# of clusters hit by the rule.
rules = collections.Counter()

# Number of hits per cluster
hits = collections.Counter()


def readOrganization(org_id):
    """Read organization for the provided organization ID."""
    if org_id in organizations.orgs:
        return organizations.orgs[org_id]
    else:
        # default value
        return "***unknown***"


# Try to open the CSV file specified.
with open(input_csv) as csv_input:
    # And open this file as CSV
    csv_reader = csv.reader(csv_input)
    rows = 0

    # Read all rows from the provided CSV file.
    for row in csv_reader:
        rows += 1
        org_id = row[0]
        cluster_id = row[1]
        raw_report = row[2]

        orgs[org_id] += 1
        clusters[cluster_id] += 1

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
                if "reports" in data:
                    hits[len(data["reports"])] += 1
                    clusters_hits[org_id] += 1
                    reports = data["reports"]
                    realRuleFound = False
                    for r in reports:
                        rule = r["component"]
                        if rule != "ccx_rules_ocm.tutorial_rule.report":
                            realRuleFound = True
                        rules[rule] += 1
                    if realRuleFound:
                        clusters_hits_no_tutorial[org_id] += 1


# Try to generate report with CSV format

# Basic statistic
print("Rows processed", rows, sep=",")
print("Unique rules found", len(rules), sep=",")
print()
print("Organizations", len(orgs), sep=",")
print("Clusters", len(clusters), sep=",")
print()

# Info about organizations
print("Top " + str(MOST_USED_ORGS) + " organizations")
print("Organization ID", "Domain", "Clusters", "Hit", "Hit/no tutorial", sep=",")

for org in orgs.most_common(MOST_USED_ORGS):
    print(org[0], readOrganization(org[0]), org[1], clusters_hits[org[0]],
          clusters_hits_no_tutorial[org[0]], sep=",")

# Info about organizations w/o Red Hat
print()
print("Top " + str(MOST_USED_ORGS) + " known organizations w/o Red Hat")
print("Organization ID", "Domain", "Clusters", "Hit", "Hit/no tutorial", sep=",")

i = 0
for org in orgs.most_common(1000000000000):
    name = readOrganization(org[0])
    if name != "***unknown***" and name != "redhat.com":
        print(org[0], readOrganization(org[0]), org[1], clusters_hits[org[0]],
              clusters_hits_no_tutorial[org[0]], sep=",")
        i += 1
    if i > MOST_USED_ORGS:
        break


# Info about rules
print()
print("Rule", "Hits", sep=",")

for rule in rules.most_common(10000):
    print(rule[0], rule[1], sep=",")

# Info about hits
print()
print("Hits", "# of clusters", sep=",")
for h in range(0, 11):
    print(h, hits[h], sep=",")

# Info about records per cluster
print()
print("Cluster", "Records", sep=",")

for cluster in clusters.most_common(20):
    print(cluster[0], cluster[1], sep=",")
