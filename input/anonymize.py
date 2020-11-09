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

"""Anonymize input data produced by OCP rules engine.

All input files that ends with '.json' are read by this script and
if they contain 'info' key, the value stored under this key is
replaced by empty list, because these informations might contain
sensitive data. Output file names are in format 's_number.json', ie.
the original file name is not preserved as it also migth contain
sensitive data.
"""

# Link to generated documentation for this script:
# <https://redhatinsights.github.io/insights-results-aggregator-utils/packages/anonymize.html>

import json
from os import listdir
from os.path import isfile, join

# Retrieve list of files in current directory.
input_files = [f for f in listdir(".") if isfile(join(".", f))]

i = 0

# Iterate over all files found in current directory.
for filename in input_files:
    # Just proper JSON files needs to be processed.
    if filename.endswith(".json"):
        # Try to open the given file, read its content, parse it as JSON and
        # use the processed payload later
        with open(filename) as fin:
            data = json.load(fin)

            # Replace content of "info" node by empty list.
            if "info" in data:
                data["info"] = []

            # Generate output JSON file
            outfilename = "s_{:0>5d}.json".format(i)
            i += 1

            # Export the updated report
            with open(outfilename, "w") as fout:
                json.dump(data, fout, indent=4)
