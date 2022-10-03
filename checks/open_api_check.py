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

"""
Simple checker for OpenAPI specification files.

usage: open_api_check.py [-h] [-v] [-n] [-d DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         make it verbose
  -n, --no-colors       disable color output
  -d DIRECTORY, --directory DIRECTORY
                        directory OpenAPI JSON file to check
"""

# Link to generated documentation for this script:
# <https://redhatinsights.github.io/insights-results-aggregator-utils/packages/open_api_check.html>

from pathlib import Path
from json import load
from sys import exit
from os import popen
from argparse import ArgumentParser
import os


def read_control_code(operation):
    """Try to execute tput to read control code for selected operation."""
    return popen("tput " + operation, "r").readline()


def empty_attribute(node, selector):
    """Test if the given attribute (of dictionary) is empty after stripping whitespaces."""
    return node[selector].strip() == ""


def check_info_node(obj, verbose):
    """Check the description in info node."""
    if verbose is not None:
        print("    checking info node")

    # Make sure we have the object (payload) deserialized.
    if obj is None:
        print("Empty object has been deserialized")
        return 1

    # Info node (with all attributes) are expected to be part of OpenAPI JSON file.
    if "info" not in obj:
        print("Info node can't be found")
        # Value to be added into error accumulator (new error has been found).
        return 1

    # Now it is possible to read info node.
    info = obj["info"]

    # Check if description attribute exists.
    if "description" not in info:
        print("No description provided for the whole file")
        # Value to be added into error accumulator (new error has been found).
        return 1

    # Check if description attribute contains any text.
    if empty_attribute(info, "description"):
        print("Empty description provided for the whole file")
        # Value to be added into error accumulator (new error has been found).
        return 1

    # Value to be added into error accumulator (no new errors).
    return 0


def check_description_for_method(path, method, m):
    """Check if description is provided for a method (endpoint + HTTP method)."""
    # Check if description attribute exists.
    if "description" not in m:
        print(
            "            No description found for endpoint `"
            + path
            + "` and method `"
            + method
            + "`"
        )
        # Value to be added into error accumulator (new error has been found).
        return 1

    # Check if description attribute contains any text.
    elif empty_attribute(m, "description"):
        print(
            "            Empty description found for endpoint `"
            + path
            + "` and method `"
            + method
            + "`"
        )
        # Value to be added into error accumulator (new error has been found).
        return 1

    # Value to be added into error accumulator (no new errors).
    return 0


def check_description_for_method_parameters(path, method, m):
    """Check if description is provided for all method parameters."""
    # Error accumulator.
    failures = 0

    if "parameters" in m:
        parameters = m["parameters"]

        # Check all parameters.
        for parameter in parameters:

            # Check if description attribute exists.
            if "description" not in parameter:
                print(
                    "            No description found for endpoint `"
                    + path
                    + "` method `"
                    + method
                    + "` and parameter `"
                    + parameter["name"]
                    + "`"
                )
                # Increase number of errors found.
                failures += 1
            # Check if description attribute contains any text.
            elif empty_attribute(parameter, "description"):
                print(
                    "            Empty description found for endpoint `"
                    + path
                    + "` method `"
                    + method
                    + "` and parameter `"
                    + parameter["name"]
                    + "`"
                )
                # Increase number of errors found.
                failures += 1

    # Return errors count for this particular check.
    return failures


def check_description_for_method_responses(path, method, m):
    """Check if description is provided for all method responses."""
    # Error accumulator.
    failures = 0

    if "responses" in m:
        responses = m["responses"]

        # Check all responses.
        for response in responses:
            r = responses[response]
            # Check if description attribute exists.
            if "description" not in r:
                print(
                    "            No description found for endpoint `"
                    + path
                    + "` method `"
                    + method
                    + "` and response `"
                    + response
                    + "`"
                )
                # Increase number of errors found.
                failures += 1
            # Check if description attribute contains any text.
            elif empty_attribute(r, "description"):
                print(
                    "            Empty description found for endpoint `"
                    + path
                    + "` method `"
                    + method
                    + "` and response `"
                    + response
                    + "`"
                )
                # Increase number of errors found.
                failures += 1

    # Return errors count for this particular check.
    return failures


def check_method(path, method, methods, verbose):
    """Check the content of HTTP method description."""
    # Error accumulator.
    failures = 0

    if verbose is not None:
        print("        checking method " + method)

    m = methods[method]

    # Perform particular error checks.
    failures += check_description_for_method(path, method, m)
    failures += check_description_for_method_parameters(path, method, m)
    failures += check_description_for_method_responses(path, method, m)

    # Return errors count for this particular check.
    return failures


def check_path(path, methods, verbose):
    """Check descriptions etc. for given path in OpenAPI file."""
    # Error accumulator.
    failures = 0

    if verbose is not None:
        print("    checking path " + path)

    # Perform error checks for all methods found in the OpenAPI file.
    for method in methods:
        # Increase number of errors found.
        failures += check_method(path, method, methods, verbose)

    # Return errors count for this particular check.
    return failures


def check_all_paths(obj, verbose):
    """Check all paths for given path in OpenAPI file."""
    # Error accumulator.
    failures = 0

    if verbose is not None:
        print("    checking all paths found in OpenAPI file")

    paths = obj["paths"]
    # Perform error checks for all paths found in the OpenAPI file.
    for path in paths:
        methods = paths[path]
        # Increase number of errors found.
        failures += check_path(path, methods, verbose)

    # Return errors count for this particular check.
    return failures


def check_openapi_json(verbose, directory):
    """Check the content of OpenAPI JSON file."""
    # Reset counters with number of passes and number of failures.
    passes = 0
    failures = 0

    filename = directory + "openapi.json"

    # If the file can be opened and loaded as JSON, everything is fine.
    with open(filename, "r") as fin:
        try:
            # Try to load and parse the content of JSON file.
            obj = load(fin)

            # At this point the JSON has been loaded and parsed correctly.
            if verbose is not None:
                print("{} has valid JSON format".format(filename))

            failures += check_info_node(obj, verbose)
            failures += check_all_paths(obj, verbose)

            if failures == 0:
                passes += 1

        except ValueError as e:
            # There are several reasons and possibilities why the file can not
            # be read as JSON, so we just print the error message taken from
            # exception object.
            print("{} has invalid JSON format".format(filename))
            failures += 1
            print(e)

    # Just the counters need to be returned because all other informations
    # about problems have been displayed already.
    return passes, failures


def display_report(passes, failures, nocolors):
    """Display report about number of passes and failures."""
    # First of all, we need to setup colors to be displayed on terminal. Colors
    # are displayed by using terminal escape control codes. When color output
    # are not enabled on command line, we can simply use empty strings in
    # output instead of real color escape codes.
    red_background = green_background = magenta_background = no_color = ""

    # If colors are enabled by command line parameter, use control sequence
    # returned by `tput` command.
    if not nocolors:
        red_background = read_control_code("setab 1")
        green_background = read_control_code("setab 2")
        magenta_background = read_control_code("setab 5")
        no_color = read_control_code("sgr0")

    # There are four possible outcomes OpenAPI check:
    # 1. no JSON files has been found
    # 2. all files are ok
    # 3. none of JSON files can be read and parsed
    # 4. some files can be read and parsed, some can not
    if failures == 0:
        if passes == 0:
            print(
                "{}[WARN]{}: no JSON files with OpenAPI detected".format(
                    magenta_background, no_color
                )
            )
        else:
            print(
                "{}[OK]{}: OpenAPI file seems to have proper format and content".format(
                    green_background, no_color
                )
            )
    else:
        print(
            "{}[FAIL]{}: file with invalid format and/or content detected".format(
                red_background, no_color
            )
        )

    # Print just number of passes and failures at the end, as this information
    # can be processed on CI.
    print("{} passes".format(passes))
    print("{} failures".format(failures))


def main():
    """Entry point to this tool."""
    # First of all, we need to specify all command line flags that are
    # recognized by this tool.
    parser = ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        help="make it verbose",
        action="store_true",
        default=None,
    )
    parser.add_argument(
        "-n",
        "--no-colors",
        dest="nocolors",
        help="disable color output",
        action="store_true",
        default=None,
    )
    parser.add_argument(
        "-d",
        "--directory",
        dest="directory",
        help="directory OpenAPI JSON file to check",
        action="store",
        default="./",
    )
    # Now it is time to parse flags, check the actual content of command line
    # and fill in the object named `args`.
    args = parser.parse_args()

    # Check JSON file containing OpenAPI specification.
    passes, failures = check_openapi_json(args.verbose, args.directory)

    # Display detailed report and summary as well.
    display_report(passes, failures, args.nocolors)

    # If any error is found, return with exit code check to non-zero value.
    if failures > 0:
        exit(1)


# If this script is started from command line, run the `main` function
# which represents entry point to the processing.
if __name__ == "__main__":
    """Entry point to this tool."""
    main()
