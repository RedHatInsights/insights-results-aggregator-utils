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

ADDRESS=localhost:8081/api/v1

curl -k -X POST -v $ADDRESS/clusters/reports -d @cluster_list_1.json
curl -k -X POST -v $ADDRESS/clusters/reports -d @cluster_list_2.json
curl -k -X POST -v $ADDRESS/clusters/reports -d @cluster_list_3.json
curl -k -X POST -v $ADDRESS/clusters/reports -d @cluster_list_4.json
curl -k -X POST -v $ADDRESS/clusters/reports -d @cluster_list_5.json
curl -k -X POST -v $ADDRESS/clusters/reports -d @cluster_list_6.json
curl -k -X POST -v $ADDRESS/clusters/reports -d @cluster_list_7.json
curl -k -X POST -v $ADDRESS/clusters/reports -d @cluster_list_8.json
curl -k -X POST -v $ADDRESS/clusters/reports -d @cluster_list_9.json
