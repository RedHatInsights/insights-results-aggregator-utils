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
Script to retrieve and analyze processing times from reports taken from external data pipeline

Usage
-----

```
usage: pta.py [-h] -i INPUT_FILE [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input INPUT_FILE
                        Specification of input file (with list of clusters,
                        for example)
  -v, --verbose         Make messages verbose
```

Example
-----

```
pta.py -i times.csv -v
```


Generated documentation in literate programming style
-----
<https://redhatinsights.github.io/insights-results-aggregator-utils/packages/pta.html>
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    df = read_timestamps(args.input_file)

    # compute durations
    df["Analysis"] = df["analyzed"] - df["last checked"]
    df["Store to database"] = df["stored"] - df["analyzed"]
    df["Total duration"] = df["stored"] - df["last checked"]

    # convert all duration series (columns) to seconds
    for duration in ("Analysis", "Store to database", "Total duration"):
        df[duration] /= np.timedelta64(1, "s")

    # print basic description of read and computed durations
    print(df.describe())

    # show plot with analysis durations
    df["Analysis"].plot(kind="line")
    plt.savefig("analysis.png")
    plt.show()

    # show plot with store to database durations
    df["Store to database"].plot(kind="line")
    plt.savefig("db_store.png")
    plt.show()

    # show plot with total durations
    df["Total duration"].plot(kind="line")
    plt.savefig("total.png")
    plt.show()

    # show histogram with analysis durations
    df.hist(column="Analysis")
    plt.savefig("analysis_hist.png")
    plt.show()

    # show histogram with store to database durations
    df.hist(column="Store to database")
    plt.savefig("db_store_hist.png")
    plt.show()

    # show histogram with total durations
    df.hist(column="Total duration")
    plt.savefig("total_hist.png")
    plt.show()


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
