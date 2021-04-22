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

# Converts structured data from JSON format into EDN format.

# Link to generated documentation for this script:
# <https://redhatinsights.github.io/insights-results-aggregator-utils/packages/json2edn.html>

import sys
import json
import edn_format

# Check if command line argument is specified (it is mandatory).
if len(sys.argv) < 2:
    print("Usage:")
    print("  json2edn.py input_file.csv")
    print("Example:")
    print("  json2edn.py report.csv")
    sys.exit(1)

# First command line argument should contain name of input JSON file.
filename = sys.argv[1]

# Try to open the JSON file specified.
with open(filename, "r") as json_input:
    # open the JSON file and parse it
    payload = json.load(json_input)
    # dump the parsed data structure into EDN format
    print(edn_format.dumps(payload))
