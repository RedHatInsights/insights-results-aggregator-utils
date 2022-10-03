"""Create an issue on github.com using the given parameters."""

# Link to generated documentation for this script:
# <https://redhatinsights.github.io/insights-results-aggregator-utils/packages/issue.html>

import os
import sys
import requests
import json

from datetime import datetime
from argparse import ArgumentParser


def current_time_formatted():
    """Prepare timestamp in a format: '2020-03-10T16:00:00Z' that is accepted by GitHub API."""
    # Retrieve current time represented in UTC time zone and format it
    # accordingly to human readable format.
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def make_github_issue(
    title,
    body=None,
    created_at=None,
    closed_at=None,
    updated_at=None,
    assignee=None,
    milestone=None,
    closed=None,
    labels=None,
    token=None,
    organization=None,
    repository=None,
):
    """Create an issue on github.com using the given parameters."""
    # URL to create issues via `POST` HTTP method.
    url = "https://api.github.com/repos/%s/%s/import/issues" % (
        organization,
        repository,
    )

    # Construct headers that need to be set.
    headers = {
        "Authorization": "token %s" % token,
        "Accept": "application/vnd.github.golden-comet-preview+json",
    }

    # Create data structure representing the issue.
    data = {
        "issue": {
            "title": title,
            "body": body,
            "created_at": created_at,
            "assignee": assignee,
        }
    }

    # The data structure needs to be converted (marshalled) into JSON format.
    payload = json.dumps(data)

    # Add the issue to the specified repository by using REST API method.
    response = requests.request("POST", url, data=payload, headers=headers)
    # Check if the issue has been created or if any error happens.
    if response.status_code == 202:
        print('Successfully created Issue "%s"' % title)
    else:
        print('Could not create Issue "%s"' % title)
        print("Response:", response.content)


def cli_arguments():
    """Retrieve all CLI arguments."""
    # First of all, we need to specify all command line flags that are
    # recognized by this tool.
    parser = ArgumentParser()

    # Authentication for user filing issue (must have read/write access to
    # repository to add issue to).
    parser.add_argument(
        "-t",
        "--token",
        dest="token",
        help="authentication token",
        action="store",
        default=None,
        type=str,
        required=True,
    )

    # The repository to add this issue to.
    parser.add_argument(
        "-o",
        "--organization",
        dest="organization",
        help="organization or repository owner",
        action="store",
        default=None,
        type=str,
        required=True,
    )
    parser.add_argument(
        "-r",
        "--repository",
        dest="repository",
        help="repository name",
        action="store",
        default=None,
        type=str,
        required=True,
    )

    # Issue-related options.
    parser.add_argument(
        "-i",
        "--title",
        dest="title",
        help="issue title",
        action="store",
        default=None,
        type=str,
        required=True,
    )

    parser.add_argument(
        "-b",
        "--body",
        dest="body",
        help="body (text) of an issue",
        action="store",
        default=None,
        type=str,
        required=True,
    )

    parser.add_argument(
        "-a",
        "--assignee",
        dest="assignee",
        help="default assignee",
        action="store",
        default=None,
        type=str,
        required=True,
    )

    # Other options.
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        help="make operations verbose",
        action="store_true",
        default=None,
    )

    # Now it is time to parse flags, check the actual content of command line
    # and fill in the object named `args`.
    return parser.parse_args()


def main():
    """Entry point to this script."""
    timestamp = current_time_formatted()
    args = cli_arguments()
    make_github_issue(
        args.title,
        body=args.body,
        created_at=timestamp,
        assignee=args.assignee,
        organization=args.organization,
        repository=args.repository,
        token=args.token,
    )


# If this script is started from command line, run the `main` function which is
# entry point to the processing.
if __name__ == "__main__":
    main()
