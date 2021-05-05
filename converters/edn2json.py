#!/usr/bin/env python3

# Copyright © 2021 Red Hat, Inc.
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

# Converts structured data from EDN format into JSON format.

# Link to generated documentation for this script:
# <https://redhatinsights.github.io/insights-results-aggregator-utils/packages/edn2json.html>

import sys
import json
import edn_format

# Check if command line argument is specified (it is mandatory).
if len(sys.argv) < 2:
    print("Usage:")
    print("  edn2json.py input_file.edn")
    print("Example:")
    print("  edn2json.py report.edn")
    sys.exit(1)

# First command line argument should contain name of input EDN file.
filename = sys.argv[1]


# Taken from https://github.com/swaroopch/edn_format/issues/76#issuecomment-749618312
def edn_to_map(x):
    if isinstance(x, edn_format.ImmutableDict):
        return {edn_to_map(k): edn_to_map(v) for k, v in x.items()}
    elif isinstance(x, edn_format.ImmutableList):
        return [edn_to_map(v) for v in x]
    elif isinstance(x, edn_format.Keyword):
        return x.name
    else:
        return x


# Try to open the EDN file specified.
with open(filename, "r") as edn_input:
    # open the EDN file and parse it
    payload = edn_format.loads(edn_input.read())
    print(json.dumps(edn_to_map(payload), indent=2))
