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

"""Script to retrieve and analyze processing times from reports taken from external data pipeline.

Description
-----

Usage
-----
```
```

Examples
-----


Generated documentation in literate programming style
-----
<https://redhatinsights.github.io/insights-results-aggregator-utils/packages/pta.html>
"""

import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import datetime

from argparse import ArgumentParser


def cli_arguments():
    """Retrieve all CLI arguments provided by user."""
    # First of all, we need to specify all command line flags that are
    # recognized by this tool.
    parser = ArgumentParser()

    # All supported command line arguments and flags
    parser.add_argument("-i", "--input", dest="input_file", default=None, required=True,
                    help="Specification of input file (with list of clusters, for example)")

    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=None,
                        help="Make messages verbose", required=False)

    # Now it is time to parse flags, check the actual content of command line
    # and fill-in the object named `args`.
    return parser.parse_args()


def main():
    """Entry point to this script."""
    # parse and process and command line arguments.
    args = cli_arguments()

    # verbosity flag
    verbose = args.verbose

    # read the data file
    timestamps = read_timestamps(args.input_file)

    # compute durations
    timestamps["analysed_duration"] = timestamps["analyzed"] - timestamps["last checked"]
    timestamps["stored_duration"] = timestamps["stored"] - timestamps["analyzed"]
    timestamps["total_duration"] = timestamps["stored"] - timestamps["last checked"]

    # print the basic description of read and computed durations
    print(timestamps.describe())


def read_timestamps(filename):
    """Read timestamps from given CSV file, parse timestamps correctly."""
    return pd.read_csv(filename,
                       date_parser=datetime_parser,
                       parse_dates=["last checked", "analyzed", "stored"])


def datetime_parser(raw_data):
    """Custom datetime parses."""
    return datetime.datetime.strptime(raw_data[:-1], "%Y-%m-%dT%H:%M:%S")



# If this script is started from command line, run the `main` function which is
# entry point to the processing.
if __name__ == "__main__":
    main()
