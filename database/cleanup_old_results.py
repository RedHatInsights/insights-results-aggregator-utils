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

r"""Prepares script to cleanup old results from database.

Description:
-----------

This script can be used to analyze data exported from `report` table by
the following command typed into PSQL console:

    \\copy report to 'reports.csv' csv

Script retrieves all reports older than the specified amount of time represented as days.
Then it creates an SQL script that can be run by administrator against selected database.

Database connection:
-------------------
Howto connect to PSQL console:

    psql -h host

Password can be retrieved from OpenShift console, for example from:
ccx-data-pipeline-qa/browse/secrets/ccx-data-pipeline-db
ccx-data-pipeline-prod/browse/secrets/ccx-data-pipeline-db

Usage:
------
    cleanup_old_results.py offset_in_days input_file.csv > cleanup.sql

Example:
-------
create a script to cleanup all records older than 90 days

    cleanup_old_results.py 90 report.csv > cleanup.sql

"""

# Link to generated documentation for this script:
# <https://redhatinsights.github.io/insights-results-aggregator-utils/packages/cleanup_old_results.html>

import sys
import csv
from datetime import datetime


# Check if command line argument is specified (it is mandatory).
if len(sys.argv) < 2:
    print("Usage:")
    print("  cleanup_old_results.py offset_in_days input_file.csv > cleanup.sql")
    print("Example:")
    print("  create a script to cleanup all records older than 90 days")
    print("  cleanup_old_results.py 90 report.csv > cleanup.sql")
    sys.exit(1)

# Column containing timestamp

# First command line argument represents offset in days
offset_in_days = int(sys.argv[1])

# Second command line argument should contain name of input CSV.
input_csv = sys.argv[2]

# End date
end_date = datetime.now()

# Try to open the CSV file specified.
with open(input_csv) as csv_input:
    # And open this file as CSV
    csv_reader = csv.reader(csv_input)
    rows = 0

    # Read all rows from the provided CSV file.
    for row in csv_reader:
        # Read all columns in one record
        org_id = row[0]
        cluster_id = row[1]
        raw_report = row[2]
        reported_at = row[3]
        last_checked_at = row[4]

        # Compute the age of the record
        reported_at = datetime.strptime(reported_at, "%Y-%m-%d %H:%M:%S.%f")
        offset = end_date - reported_at

        # If the record is older than specified offset (relative time), add
        # that record into generated script
        if offset.days >= offset_in_days:
            print(
                "-- {} {} {} {}".format(
                    org_id, cluster_id, reported_at, last_checked_at
                )
            )
            print(
                "delete from reports where org_id={} and cluster_id='{}'".format(
                    org_id, cluster_id
                )
            )
            print()

# Finito
