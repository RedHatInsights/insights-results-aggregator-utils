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

"""Plots histogram displaying distribution of the first digit in cluster ID."""

import sys
import csv
import matplotlib.pyplot as plt
import numpy

# Check if command line argument is specified (it is mandatory).
if len(sys.argv) < 2:
    print("Usage:")
    print("  cluster_id_distribution.py input_file.csv")
    print("Example:")
    print("  cluster_id_distribution.py report.csv")
    sys.exit(1)

# First command line argument should contain name of input CSV.
input_csv = sys.argv[1]

# must be n+1
bins = range(0, 17)

# Try to open the CSV file specified.
with open(input_csv) as csv_input:
    # And open this file as CSV
    csv_reader = csv.reader(csv_input)
    rows = 0

    # Read all rows from the provided CSV file
    # and read just first digits from cluster IDs
    digits = [int(row[1][1], 16) for row in csv_reader]
    print(digits)

# Compute histogram
hist, _ = numpy.histogram(digits, bins=bins, range=None, density=False)

# Display histogram as a table
for i, v in enumerate(hist):
    print(i, v)

# Create new histogram graph
plt.hist(digits, bins=bins, range=None, density=False, rwidth=0.9)

# Dirty trick - move ticks by 1/2 so they are displayed in middle of columns
plt.xticks(numpy.arange(0, 16)+0.5, range(0, 16), fontsize=7)

# Add a grid
plt.grid(axis='y', alpha=0.50)

# Title of a graph
plt.title("Distribution of the first digit in cluster IDs")

# Add a label to x-axis
plt.xlabel("First digit from cluster ID")

# Add a label to y-axis
plt.ylabel("Usage of the digit")

# Set the plot layout
plt.tight_layout()

# And save the plot into raster format and vector format as well
plt.savefig("id_distribution.png")
plt.savefig("id_distribution.svg")

# Try to show the plot on screen
plt.show()
