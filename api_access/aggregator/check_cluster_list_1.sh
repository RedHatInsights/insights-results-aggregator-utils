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

ADDRESS=localhost:8080/api/v1

curl -k -X GET -v $ADDRESS/organizations/1/clusters/123/reports
curl -k -X GET -v $ADDRESS/organizations/1/clusters/123,456/reports
curl -k -X GET -v $ADDRESS/organizations/1/clusters/123,456,/reports
curl -k -X GET -v $ADDRESS/organizations/1/clusters/00000000-0000-0000-0000-000000000000/reports
curl -k -X GET -v $ADDRESS/organizations/1/clusters/00000000-0000-0000-0000-000000000000,00000000-0000-0000-0000-ffffffffffff/reports
curl -k -X GET -v $ADDRESS/organizations/1/clusters/00000000-0000-0000-0000-000000000000,00000000-0000-0000-0000-ffffffffffff,00000000-0000-0000-ffff-000000000000/reports
curl -k -X GET -v $ADDRESS/organizations/1/clusters/00000000-0000-0000-0000-000000000000,00000000-0000-0000-0000-ffffffffffff,00000000-0000-0000-ffff-000000000000/reports
curl -k -X GET -v $ADDRESS/organizations/1/clusters/00000000-0000-0000-0000-000000000000,00000000-0000-0000-0000-ffffffffffff,00000000-0000-0000-ffff-000000000000,aaaaaaaa-bbbb-cccc-dddd-ffffffffffff/reports
curl -k -X GET -v $ADDRESS/organizations/1/clusters/aaaaaaaa-bbbb-cccc-dddd-ffffffffffff/reports
curl -k -X GET -v $ADDRESS/organizations/1/clusters/5d5892d3-1f74-4ccf-91af-548dfc9767ab/reports
curl -k -X GET -v $ADDRESS/organizations/1/clusters/00000000-0000-0000-0000-000000000000,5d5892d3-1f74-4ccf-91af-548dfc9767ab/reports
curl -k -X GET -v $ADDRESS/organizations/1/clusters/00000000-0000-0000-0000-000000000000,5d5892d3-1f74-4ccf-91af-548dfc9767ab,b0c2d108-0603-41c3-9a8f-0a37eba5df49/reports
curl -k -X GET -v $ADDRESS/organizations/1/clusters/00000000-0000-0000-0000-000000000000,5d5892d3-1f74-4ccf-91af-548dfc9767ab,b0c2d108-0603-41c3-9a8f-0a37eba5df49,5d5892d3-1f74-4ccf-91af-548dfc9767aa/reports
