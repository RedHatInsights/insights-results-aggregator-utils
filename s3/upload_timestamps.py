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

"""Script to retrieve timestamp of all objects stored in AWS S3 bucket and export them to CSV."""

# Link to generated documentation for this script:
# <https://redhatinsights.github.io/insights-results-aggregator-utils/packages/upload_timestamps.html>

import boto3
import botocore
import csv
import sys
from argparse import ArgumentParser


def connect_to_s3(aws_access_key_id, aws_secret_access_key, region_name):
    """Try to connect into AWS S3 and initialize new session."""
    # Construction and initialization of session into AWS S3.
    session = boto3.session.Session(aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key,
                                    region_name=region_name)

    # These two configuration options are set to constants, but it might be
    # possible that it will be configurable later.
    use_ssl = True
    endpoint_url = None

    # Retrieve the 's3' resource which represents the real session object.
    return session.resource('s3',
                            config=botocore.client.Config(signature_version='s3v4'),
                            use_ssl=use_ssl, endpoint_url=endpoint_url)


def get_list_of_timestamps(s3_session, bucket_name, max_records=None):
    """Get a list of timestamps for all objects in selected S3 bucket."""
    # Construct object that represents the bucket in S3.
    bucket = s3_session.Bucket(bucket_name)

    n = 0
    timestamps = []

    # Iterate over all objects found in given bucket. Please be avare that this
    # operation might be time and/or memory consuming.
    for obj in bucket.objects.all():
        timestamps.append(obj.last_modified)

        # It is possible to limit number of records. If `max_records` is set to
        # `None`, limits are not used.
        if max_records is not None:
            n += 1
            if n >= max_records:
                break

    return timestamps


def export_timestamps_into_csv(csv_file_name, timestamps):
    """Export timestamps into CSV file."""
    # Try to open new file for writing.
    with open(csv_file_name, 'w') as csvfile:
        # Initialize CSV writer.
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)

        # First row with header.
        writer.writerow(["Timestamp"])

        # And write all timestamps into the CSV file.
        for timestamp in timestamps:
            writer.writerow([timestamp])


def cli_arguments():
    """Retrieve all CLI arguments."""
    # First of all, we need to specify all command line flags that are
    # recognized by this tool.
    parser = ArgumentParser()
    parser.add_argument("-k", "--access_key", help="AWS access key ID", required=True)
    parser.add_argument("-s", "--secret_key", help="AWS secret access key", required=True)
    parser.add_argument("-r", "--region", help="AWS region, us-east-1 by default",
                        default="us-east-1")
    parser.add_argument("-b", "--bucket",
                        help="bucket name, insights-buck-it-openshift by default",
                        default="insights-buck-it-openshift")
    parser.add_argument("-o", "--output", help="output file name", required=True)
    parser.add_argument("-m", "--max_records", help="max records to export (default=all)",
                        default=None, type=int)

    # Now it is time to parse flags, check the actual content of command line
    # and fill in the object named `args`.
    return parser.parse_args()


def main():
    """Entry point to this script."""
    # Parse and process and command line arguments.
    args = cli_arguments()

    # Initialize S3 session and read all timestamps.
    s3 = connect_to_s3(args.access_key, args.secret_key, args.region)
    timestamps = get_list_of_timestamps(s3, args.bucket, args.max_records)

    # Timestamps are usually not sorted, so we need to sort them explicitly.
    timestamps.sort()

    # Finally, export all timestamps into specified file.
    export_timestamps_into_csv(args.output, timestamps)


# If this script is started from command line, run the `main` function which is
# entry point to the processing.
if __name__ == "__main__":
    main()
