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

"""Script to retrieve memory and GC statistic from the standard Go metrics.

Memory and GC statistic is being exported into CSV file to be further processed.
"""

import csv
import requests
import time

from argparse import ArgumentParser
from prometheus_client.parser import text_string_to_metric_families

# all exported metrics
exported_metrics = (
        "go_gc_duration_seconds_sum",
        "go_gc_duration_seconds_count",
        "go_memstats_alloc_bytes",
        "go_memstats_sys_bytes",
        "go_memstats_mallocs_total",
        "go_memstats_frees_total",
        )


def parse_metrics(exported_metrics, payload):
    """Parse metrics from payload returned from the monitored service."""
    metrics = []
    for family in text_string_to_metric_families(str(payload)):
        for sample in family.samples:
            name, labels, value = sample
            # try to find all metrics that need to be exported
            for exported_metric in exported_metrics:
                if exported_metric == name:
                    metrics.append(value)
    return metrics


def monitor_service(exported_metric, url, csv_filename, sleep_amount, max_records):
    """Monitor selected service and export retrieved metrics into CSV file."""
    with open(csv_filename, 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(exported_metrics)

        n = 0

        while True:
            payload = requests.get("http://localhost:8080/api/v1/metrics").text
            metrics = parse_metrics(exported_metrics, payload)
            writer.writerow(metrics)

            # make sure the next Ctrl+C or kill won't affect more that the last record
            csvfile.flush()
            print("recorded")

            time.sleep(sleep_amount)

            # it is possible to limit number of records
            if max_records is not None:
                n += 1
                if n >= max_records:
                    print("done")
                    break


def cli_arguments():
    """Retrieve all CLI arguments."""
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", help="URL to get metrics",
                        default="http://localhost:8080/api/v1/metrics", type=str)
    parser.add_argument("-o", "--output", help="output file name", required=True)
    parser.add_argument("-d", "--delay", help="Delay in seconds between records",
                        default=5, type=int)
    parser.add_argument("-m", "--max_records", help="max records to export (default=all)",
                        default=None, type=int)

    return parser.parse_args()


def main():
    """Entry point to this script."""
    args = cli_arguments()
    monitor_service(exported_metrics, args.url, args.output, args.delay, args.max_records)


if __name__ == "__main__":
    main()
