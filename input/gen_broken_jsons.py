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

"""Generate messages to be consumed by aggregator that are not proper JSONs.

This script read input message (that should be correct) and generates bunch of
new messages. Each generated message is broken - it does not contain proper
JSON object - to test how broken messages are handled on aggregator
(ie. consumer) side.

Types of input message mutation:
* any item (identified by its key) can be removed
* new items with random key and content can be added
* any item can be replaced by new random content
"""

import json
import os
import sys
import copy
import itertools
import random
from argparse import ArgumentParser

DEFAULT_NUMBER_OF_EXPORTED_JSONS = 10
DEFAULT_NEW_LINE_PROBABILITY = 10
DEFAULT_DELETE_LINE_PROBABILITY = 10
DEFAULT_MUTATE_LINE_PROBABILITY = 20


def load_input(filename, verbose):
    """Load JSON file as a regular text file."""
    if verbose:
        print("Loading original file", filename)
    with open(filename) as fin:
        return fin.readlines()


def generate_output(filename, payload, verbose):
    """Generate output file."""
    with open(filename, 'w') as fout:
        for line in payload:
            fout.write(line)
        if verbose:
            print("Generated file {}".format(filename))


def shuffle_lines(payload, verbose):
    """Shuffle lines in the payload to produce possibly broken JSON."""
    if verbose:
        print("    shuffling lines")
    random.shuffle(payload)


def add_random_lines(payload, new_line_probability, verbose):
    """Add random lines into the payload to produce possible broken JSON."""
    res = []
    i = 1
    for line in payload:
        res.append(line)
        if random.random()*100 < new_line_probability:
            if verbose:
                print("    appending error line at position", i)
            res.append("ERROR_LINE\n")
        i += 1
    return res


def is_structure_line(line):
    """Check if the given line defines 'structure' in JSON - node opening or closing."""
    return line.endswith(" },\n") or line.endswith("{\n")


def delete_random_lines(payload, delete_line_probability, verbose):
    """Delete random lines from the payload to produce possible broken JSON."""
    res = []
    i = 1
    for line in payload:
        if random.random()*100 < delete_line_probability and is_structure_line(line):
            if verbose:
                print("    deleting line from position", i)
        else:
            res.append(line)
        i += 1
    return res


def mutate_lines(payload, mutate_line_probability, verbose):
    """Mutate lines in the payload to produce possible broken JSON."""
    res = []
    i = 1
    for line in payload:
        if random.random()*100 < mutate_line_probability:
            i = int(len(line) * random.random())
            line = line[:i] + "***FOO***" + line[i:]
            if verbose:
                print("    mutating line", i)
        res.append(line)
        i += 1
    return res


def is_proper_json(payload):
    """Check whether the payload represents proper JSON or not."""
    try:
        s = "".join(payload)
        obj = json.loads(s)
        return True
    except Exception as e:
        print(e)
        return False


def cli_arguments():
    """Retrieve all CLI arguments."""
    parser = ArgumentParser()

    parser.add_argument("-i", "--input", dest="input", help="name of input file",
                        action="store", default=None, type=str, required=True)
    parser.add_argument("-o", "--output", dest="output",
                        help="template for output file name (default out_{}.json)",
                        action="store", default="out_{}.json", type=str)
    parser.add_argument("-e", "--exported", dest="exported",
                        help="number of JSONs to be exported (10 by default)",
                        action="store", default=10, type=int, required=False)
    parser.add_argument("-v", "--verbose", dest="verbose", help="make it verbose",
                        action="store_true", default=None)
    parser.add_argument("-s", "--shuffle_lines", dest="shuffle_lines",
                        help="shufffle lines to produce improper JSON",
                        action="store_true", default=None)
    parser.add_argument("-a", "--add_lines", dest="add_lines",
                        help="add random lines to produce improper JSON",
                        action="store_true", default=None)
    parser.add_argument("-d", "--delete_lines", dest="delete_lines",
                        help="delete randomly selected lines to produce improper JSON",
                        action="store_true", default=None)
    parser.add_argument("-m", "--mutate_lines", dest="mutate_lines",
                        help="mutate lines individually",
                        action="store_true", default=None)
    parser.add_argument("-ap", "--add_line_probability", dest="add_line_probability",
                        help="probability of new line to be added (0-100)",
                        default=DEFAULT_NEW_LINE_PROBABILITY, type=int)
    parser.add_argument("-dp", "--delete_line_probability", dest="delete_line_probability",
                        help="probability of line to be deleted (0-100)",
                        default=DEFAULT_DELETE_LINE_PROBABILITY, type=int)
    parser.add_argument("-mp", "--mutate_line_probability", dest="mutate_line_probability",
                        help="probability of line to be mutate (0-100)",
                        default=DEFAULT_MUTATE_LINE_PROBABILITY, type=int)

    return parser.parse_args()


def mutate_payload(args):
    """Load original JSON file and mutate it in many ways."""
    payload = load_input(args.input, args.verbose)

    if args.shuffle_lines:
        shuffle_lines(payload, args.verbose)
    if args.add_lines:
        payload = add_random_lines(payload, args.add_line_probability, args.verbose)
    if args.delete_lines:
        payload = delete_random_lines(payload, args.delete_line_probability, args.verbose)
    if args.mutate_lines:
        payload = mutate_lines(payload, args.mutate_line_probability, args.verbose)
        return payload


def main(filename):
    """Entry point to this script."""
    args = cli_arguments()
    verbose = args.verbose
    max_exported = args.exported

    exported = 0
    while exported < max_exported:
        payload = mutate_payload(args)
        if not is_proper_json(payload):
            filename = args.output.format(exported+1)
            if verbose:
                print("Generating", filename)
            generate_output(filename, payload, verbose)
            exported += 1


if len(sys.argv) < 2:
    print("Usage: python gen_broken_messages.py input_file.json")
    sys.exit(1)

main(sys.argv[1])
