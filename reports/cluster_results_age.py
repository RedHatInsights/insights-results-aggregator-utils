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

"""Creates plot (graph) displaying statistic about the age of rule results."""

# Link to generated documentation for this script:
# <https://redhatinsights.github.io/insights-results-aggregator-utils/packages/cluster_results_age.html>

import sys
import csv
import collections
from datetime import datetime
import matplotlib.pyplot as plt

days_stat = collections.Counter()

# Check if command line argument is specified (it is mandatory).
if len(sys.argv) < 2:
    print("Usage:")
    print("  reports.py input_file.csv")
    print("Example:")
    print("  reports.py report.csv")
    sys.exit(1)

# First command line argument should contain name of input CSV.
input_csv = sys.argv[1]

# End date (can be set to time.Now() if required)
d2 = datetime.strptime("2020-07-31", "%Y-%m-%d")

# Try to open the CSV file specified.
with open(input_csv) as csv_input:
    # And open this file as CSV
    csv_reader = csv.reader(csv_input)
    rows = 0

    # Read all rows from the provided CSV file.
    for row in csv_reader:
        rows += 1
        d1 = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
        offset = d2 - d1
        days_stat[offset.days] += 1

# Prepare data for x-y plot
days = sorted(days_stat.keys())
counts = [days_stat[day] for day in days]

# Create new line x-y plot
plt.plot(days, counts, "-", markersize=2)

# Add a label to x-axis
plt.xlabel("Result age (days)")

# Add a label to y-axis
plt.ylabel("Number of clusters")

# Set the plot layout
plt.tight_layout()

# And save the plot into raster format and vector format as well
plt.savefig("results_age.png")
plt.savefig("results_age.svg")

# Try to show the plot on screen
plt.show()
