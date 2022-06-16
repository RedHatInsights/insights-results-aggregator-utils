#!/bin/bash
# Copyright 2020 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

N_FILES=$(find output -mindepth 1 -type f -name "*.json" -printf x | wc -c)
# Continuously generate messages
while true
do
    # All JSON files in current directory will be sent to Kafka via Kafkacat
    i=0
    for file in output/*.json 
    do
        # Update the port accordingly (this one is for Kafka running inside Docker)
        kafkacat -b localhost:9092 -P -t ccx.ocp.results $file
        # It is possible to change the sleep value (or remove it completely)
        # sleep 1
        echo $i
        i=$((i+1))
    done | tqdm --total "$N_FILES" >> /dev/null
    exit 0
done
