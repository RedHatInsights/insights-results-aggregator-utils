#!/usr/bin/env python3

# Copyright © 2020 Pavel Tisnovsky
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

"""Plot graph with Kafka lags with linear regression line added into plot.

Source CSV file is to be retrieved from Grafana.

Usage:
-----
kafka_lags.py input_file.csv

Example:
-------
kafka_lags.py overall.csv")

"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Standard moving average window
sma_window = 50

# Check if command line argument is specified (it is mandatory).
if len(sys.argv) < 2:
    print("Usage:")
    print("  plot_kafka_lags_pandas.py input_file.csv")
    print("Example:")
    print("  plot_kafka_lags_pandas.py overall.csv")
    sys.exit(1)

# First command line argument should contain name of input CSV.
input_csv = sys.argv[1]

# Try to open the CSV file specified.
df = pd.read_csv(input_csv)

# Add a standard moving average column
df["SMA"] = df.iloc[:, 1].rolling(window=sma_window).mean()

# Print the data frame and its description as well
print(df.info())
print()
print(df.describe())

# Values to be plotted
time = df["Time"]
messages = df["topic : uploads"]
sma = df["SMA"]

# Linear regression
x = np.arange(0, len(messages))
coef = np.polyfit(x, messages, 1)
poly1d_fn = np.poly1d(coef)

# Create new graph
plt.plot(messages, "-", poly1d_fn(np.arange(0, len(messages))), "r-")

# Title of a graph
plt.title("Messages in Kafka")

# Add a label to x-axis
plt.xlabel("Time")

# Add a label to y-axis
plt.ylabel("Messages")

plt.legend(loc="upper right")

# Set the plot layout
plt.tight_layout()

# And save the plot into raster format and vector format as well
plt.savefig("kafka_lags_pandas.png")
plt.savefig("kafka_lags_pandas.svg")

# Try to show the plot on screen
plt.show()

# Create new graph
plt.plot(sma, "-", poly1d_fn(np.arange(0, len(messages))), "r-")

# Title of a graph
plt.title("Messages in Kafka")

# Add a label to x-axis
plt.xlabel("Time")

# Add a label to y-axis
plt.ylabel("Messages")

# Specify legend placement
plt.legend(loc="upper right")

# Set the plot layout
plt.tight_layout()

# And save the plot into raster format and vector format as well
plt.savefig("kafka_lags_pandas_sma.png")
plt.savefig("kafka_lags_pandas_sma.svg")

# Try to show the plot on screen
plt.show()
