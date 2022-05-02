# insights-results-aggregator-utils
Utilities for Insights Results Aggregator

[![GitHub Pages](https://img.shields.io/badge/%20-GitHub%20Pages-informational)](https://redhatinsights.github.io/insights-results-aggregator-utils/)
[![License](https://img.shields.io/badge/license-Apache-blue)](https://github.com/RedHatInsights/insights-results-aggregator-utils/blob/master/LICENSE)

<!-- vim-markdown-toc GFM -->

* [Utilities for accessing REST API endpoints for selected services](#utilities-for-accessing-rest-api-endpoints-for-selected-services)
    * [`aggregator/check_cluster_list_1.sh`](#aggregatorcheck_cluster_list_1sh)
        * [Description](#description)
        * [Remark](#remark)
    * [`aggregator/check_cluster_list_2.sh`](#aggregatorcheck_cluster_list_2sh)
        * [Description](#description-1)
        * [Remark](#remark-1)
    * [`smart_proxy/check_cluster_list_1.sh`](#smart_proxycheck_cluster_list_1sh)
        * [Description](#description-2)
        * [Remark](#remark-2)
    * [`smart_proxy/check_cluster_list_2.sh`](#smart_proxycheck_cluster_list_2sh)
        * [Description](#description-3)
        * [Remark](#remark-3)
* [Utilities for handling messages to be consumed by aggregator](#utilities-for-handling-messages-to-be-consumed-by-aggregator)
    * [`anonymize.py`](#anonymizepy)
        * [Description](#description-4)
        * [Generated documentation](#generated-documentation)
        * [Usage](#usage)
    * [`2report.py`](#2reportpy)
        * [Description](#description-5)
        * [Generated documentation](#generated-documentation-1)
        * [Usage](#usage-1)
    * [`fill_in_results.sh`](#fill_in_resultssh)
        * [Description](#description-6)
        * [Generated documentation](#generated-documentation-2)
        * [Usage](#usage-2)
        * [A real example](#a-real-example)
    * [`gen_broken_messages.py`](#gen_broken_messagespy)
        * [Description](#description-7)
        * [Generated documentation](#generated-documentation-3)
        * [Usage](#usage-3)
    * [`gen_broken_jsons.py`](#gen_broken_jsonspy)
        * [Description](#description-8)
        * [Generated documentation](#generated-documentation-4)
        * [Usage](#usage-4)
    * [`random_payload_generator.py`](#random_payload_generatorpy)
        * [Description](#description-9)
        * [Generated documentation](#generated-documentation-5)
        * [Usage](#usage-5)
* [Utilitites for generating reports etc.](#utilitites-for-generating-reports-etc)
    * [`stat.py`](#statpy)
        * [Description](#description-10)
        * [Generated documentation](#generated-documentation-6)
        * [Usage](#usage-6)
    * [`affected_clusters.py`](#affected_clusterspy)
        * [Description](#description-11)
        * [Generated documentation](#generated-documentation-7)
        * [Usage](#usage-7)
    * [`reports.py`](#reportspy)
        * [Description](#description-12)
        * [Generated documentatin](#generated-documentatin)
        * [Usage](#usage-8)
    * [`cluster_results_age.py`](#cluster_results_agepy)
        * [Description](#description-13)
        * [Generated documentatin](#generated-documentatin-1)
        * [Usage](#usage-9)
* [Utilities for working with objects stored in AWS S3 bucket](#utilities-for-working-with-objects-stored-in-aws-s3-bucket)
    * [`upload_timestamps.py`](#upload_timestampspy)
        * [Description](#description-14)
        * [Generated documentation](#generated-documentation-8)
        * [Usage](#usage-10)
    * [`download_prod_data`](#download_prod_data)
        * [Description](#description-15)
        * [Generated documentation](#generated-documentation-9)
        * [Usage](#usage-11)
* [Monitoring tools](#monitoring-tools)
    * [`go_metrics.py`](#go_metricspy)
        * [Generated documentation](#generated-documentation-10)
        * [Usage](#usage-12)
    * [`kafka_lags.py`](#kafka_lagspy)
        * [Generated documentation](#generated-documentation-11)
        * [Usage](#usage-13)
        * [Example](#example)
* [Checking tools](#checking-tools)
    * [`json_check.py`](#json_checkpy)
        * [Usage](#usage-14)
        * [Generated documentation](#generated-documentation-12)
* [Database related tools](#database-related-tools)
    * [`cleanup_old_results.py`](#cleanup_old_resultspy)
        * [Description](#description-16)
        * [Generated documentation](#generated-documentation-13)
        * [Database connection](#database-connection)
        * [Usage](#usage-15)
        * [Example](#example-1)
* [Package manifest](#package-manifest)

<!-- vim-markdown-toc -->

## Utilities for accessing REST API endpoints for selected services

These utilities are stored in `api_access` subdirectory.

### `aggregator/check_cluster_list_1.sh`

#### Description

BASH script to retrieve results for multiple clusters (specified in URL) from the Insights Results Aggregator service.

#### Remark

It is needed to provide the correct value for variable `ADDRESS` that should points to running Insights Result Aggregator service instance.



### `aggregator/check_cluster_list_2.sh`

#### Description

BASH script to retrieve results for multiple clusters (specified in request payload) from the Insights Results Aggregator service.

#### Remark

It is needed to provide the correct value for variable `ADDRESS` that should points to running Insights Result Aggregator service instance.



### `smart_proxy/check_cluster_list_1.sh`

#### Description

BASH script to retrieve results for multiple clusters (specified in URL) from the Smart Proxy service.

#### Remark

It is needed to provide the correct value for variable `ADDRESS` that should points to running Smart Proxy service instance.



### `smart_proxy/check_cluster_list_2.sh`

#### Description

BASH script to retrieve results for multiple clusters (specified in request payload) from the Smart Proxy service.

#### Remark

It is needed to provide the correct value for variable `ADDRESS` that should points to running Smart Proxy service instance.



------------------------------------------------------------------------------

## Utilities for handling messages to be consumed by aggregator

These utilities are stored in `input` subdirectory.



### `anonymize.py`

Anonymize input data produced by OCP rules engine.

#### Description

All input files that ends with '.json' are read by this script and
if they contain 'info' key, the value stored under this key is
replaced by empty list, because these informations might contain
sensitive data. Output file names are in format 's_number.json', ie.
the original file name is not preserved as it also might contain
sensitive data.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/anonymize.html

#### Usage

```
python3 anonymize.py
```

------------------------------------------------------------------------------



### `2report.py`

Converts outputs from OCP rule engine into proper reports.

#### Description

All input files that with filename 's_\*.json' (usually anonymized
outputs from OCP rule engine' are converted into proper 'report'
that can be:

1. Published into Kafka topic
1. Stored directly into aggregator database

It is done by inserting organization ID, clusterName and lastChecked
attributes and by rearanging output structure. Output files will
have following names: 'r_\*.json'.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/2report.html

#### Usage

```
python3 2report.py
```

------------------------------------------------------------------------------



### `fill_in_results.sh`

This script can be used to fill in the aggregator database in the selected pipeline with data taken from test clusters.

#### Description

The script performs several operations:

1. Decompress input data generated by Insights operator and stored in Ceph/AWS bucket, update directory structure accordingly
1. Run Insights OCP rules against all input data
1. Anonymize OCP rules results
1. Convert OCP rules results into a form compatible with aggregator. These results (JSONs) can be published into Kafka using `produce.sh` (several times if needed)

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/fill_in_results.html

#### Usage

```shell
./fill_in_results.sh archive.tar.bz org_id cluster_name
```

#### A real example

```shell
./fill_in_results.sh external-rules-archives-2020-03-31.tar 11789772 5d5892d3-1f74-4ccf-91af-548dfc9767aa
```

------------------------------------------------------------------------------

### `gen_messages.py`

Generates messages to be consumed by Insights Results Aggregator.

#### Description

This script read input message (that should be correct or incorrect, according
to needs) and generates bunch of new messages derived from input one. Each
generated message can be updated if needed - Org ID can changed, cluster ID can
changed as well etc.

Types of possible input message modification:
    * Org ID (if enabled by CLI flag -g)
    * Account number (if enabled by CLI flag -a)
    * Cluster ID (if enabled by CLI flag -c)

It is also possible to specify pattern for output message filenames. For example:
`generated_message_{}.json`

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/gen_messages.html

#### Usage

```
usage: gen_messages.py [-h] [-i INPUT] [-o OUTPUT] [-r REPEAT] [-g] [-a] [-c] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Specification of input file
  -o OUTPUT, -output OUTPUT
                        Specification of pattern of output file names
  -r REPEAT, --repeat REPEAT
                        Number of generated files
  -g, --org-id          Enable organization ID modification
  -a, --account-number  Enable account number modification
  -c, --cluster-id      Enable cluster ID modification
  -v, --verbose         Make messages verbose
```


------------------------------------------------------------------------------



### `gen_broken_messages.py`

This script read input message (that should be correct) and generates bunch of new messages.

#### Description

Each generated message is broken in some way so it is possible to use such messages to test how broken messages are handled on aggregator (ie. consumer) side.

Types of input message mutation:
* any item (identified by its key) can be removed
* new items with random key and content can be added
* any item can be replaced by new random content

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/gen_broken_messages.html

#### Usage

```
python gen_broken_messages.py input_file.json
```

------------------------------------------------------------------------------



### `gen_broken_jsons.py`

This script read input message (that should be correct) and generates bunch of new messages.

#### Description

Each generated message is broken - it does not contain proper JSON object - to test how broken messages are handled on aggregator (ie. consumer) side.

Types of input message mutation:
* any item (identified by its key) can be removed
* new items with random key and content can be added
* any item can be replaced by new random content

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/gen_broken_jsons.html

#### Usage

```
usage: gen_broken_jsons.py [-h] -i INPUT [-o OUTPUT] [-e EXPORTED] [-v] [-s]
                           [-a] [-d] [-m] [-ap ADD_LINE_PROBABILITY]
                           [-dp DELETE_LINE_PROBABILITY]
                           [-mp MUTATE_LINE_PROBABILITY]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        name of input file
  -o OUTPUT, --output OUTPUT
                        template for output file name (default out_{}.json)
  -e EXPORTED, --exported EXPORTED
                        number of JSONs to be exported (10 by default)
  -v, --verbose         make it verbose
  -s, --shuffle_lines   shufffle lines to produce improper JSON
  -a, --add_lines       add random lines to produce improper JSON
  -d, --delete_lines    delete randomly selected lines to produce improper
                        JSON
  -m, --mutate_lines    mutate lines individually
  -ap ADD_LINE_PROBABILITY, --add_line_probability ADD_LINE_PROBABILITY
                        probability of new line to be added (0-100)
  -dp DELETE_LINE_PROBABILITY, --delete_line_probability DELETE_LINE_PROBABILITY
                        probability of line to be deleted (0-100)
  -mp MUTATE_LINE_PROBABILITY, --mutate_line_probability MUTATE_LINE_PROBABILITY
                        probability of line to be mutate (0-100)
```

------------------------------------------------------------------------------


### `random_payload_generator.py`

Generator of random payload for testing REST API, message consumers, test frameworks etc.

#### Description

This source file contains class named `RandomPayloadGenerator` that can be reused by other scripts and tools to generate random payloed, useful for testing, implementing fuzzers etc.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/random_payload_generator.html

#### Usage

This is a helper class that can't be started directly from the command line. Internally it is used by script `gen_broken_messages.py`.

------------------------------------------------------------------------------



## Utilitites for generating reports etc.

These utilities are stored in `reports` subdirectory.



### `stat.py`

Display statistic about rules that really 'hit' problems on clusters.

#### Description

This script can be used to display statistic about rules that really 'hit' problems on clusters. Can be used against test data or production data if needed.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/stat.html

#### Usage

To run this tool against all files in current directory that contains test data or production data:

```
python3 stat.py
```

------------------------------------------------------------------------------



### `affected_clusters.py`

Analyze data exported from `db-writer` database.

#### Description

This script can be used to analyze data exported from `report` table by
the following command typed into PSQL console:

    \copy report to 'reports.csv csv

Script displays two tables:
    1. org id + cluster name (list of affected clusters)
    2. org id + number of affected clusters (usually the only information reguired by management)

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/affected_clusters.html

#### Usage


```
Usage:
  affected_clusters.py rule_name input_file.csv
Example:
  affected_clusters.py ccx_rules_ocp.external.bug_rules.bug_12345678.report report.csv
```

------------------------------------------------------------------------------



### `reports.py`

Analyze data exported from `db-writer` database.

#### Description

List all rules and other interesting informations found in reports.csv. Data
are exported into CSV format so it will be possible to include them in
spreadsheets.


#### Generated documentatin

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/reports.html

#### Usage

```

This script can be used to analyze data exported from `report` table by
the following command typed into PSQL console:

    \copy report to 'reports.csv' csv

Howto connect to PSQL console:
    psql -h host

Password can be retrieved from OpenShift console, for example from:
ccx-data-pipeline-qa/browse/secrets/ccx-data-pipeline-db
ccx-data-pipeline-prod/browse/secrets/ccx-data-pipeline-db
```

------------------------------------------------------------------------------



### `cluster_results_age.py`

Creates plot (graph) displaying statistic about the age of rule results.

#### Description

Creates plot (graph) displaying statistic about the age of rule results.


#### Generated documentatin

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/cluster_results_age.html

#### Usage

```

python3 cluster_results_age.py input.csv
```

------------------------------------------------------------------------------



## Utilities for working with objects stored in AWS S3 bucket

These utilities are stored in `s3` subdirectory.



### `upload_timestamps.py`

Script to retrieve timestamp of all objects stored in AWS S3 bucket and export them to CSV.

#### Description

This script retrieves timestamps of all objects that are stored in AWS S3 bucket and export these timestamps to CSV file.
It is possible to specify region (in S3), access key, and secret key.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/upload_timestamps.html

#### Usage

```
upload_timestamps.py [-h] -k ACCESS_KEY -s SECRET_KEY [-r REGION]
                     [-b BUCKET] -o OUTPUT [-m MAX_RECORDS]

optional arguments:
  -h, --help            show this help message and exit
  -k ACCESS_KEY, --access_key ACCESS_KEY
                        AWS access key ID
  -s SECRET_KEY, --secret_key SECRET_KEY
                        AWS secret access key
  -r REGION, --region REGION
                        AWS region, us-east-1 by default
  -b BUCKET, --bucket BUCKET
                        bucket name, insights-buck-it-openshift by default
  -o OUTPUT, --output OUTPUT
                        output file name
  -m MAX_RECORDS, --max_records MAX_RECORDS
                        max records to export (default=all)
```

### `download_prod_data`

Script to download N tarballs from M clusters from external data pipeline bucket.

#### Description

This script is used to download tarballs stored in AWS S3 bucket and export the clusters and tarball path to a CSV.
It is fully configurable although it expects the bucket to have a format `s3://BUCKET/SUPER_FOLDER/CLUSTER/...`.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/upload_timestamps.html

#### Usage

```
❯ cd s3/download_prod_data
❯ go build .
❯ ./download_prod_data --help
Usage of ./download_prod_data:
  -access-key string
        access key
  -bucket string
        bucket name
  -disable-ssl
        whether to disable SSL or not (default false)
  -endpoint string
        endpoint (leave empty to use AWS)
  -n-clusters int
        number of clusters (default 1)
  -n-tarballs int
        number of tarballs per cluster (default 1)
  -output string
        path to save the CSV file
  -prefix string
        path to the clusters folders
  -region string
        bucket region (default "us-east-1")
  -secret-key string
        secret key
```

You can also `go run main.go`, it is not mandatory to build it.

------------------------------------------------------------------------------



## Monitoring tools

These utilities are stored in `monitoring` subdirectory.



### `go_metrics.py`

Script to retrieve memory and GC statistic from the standard Go metrics. Memory and GC statistic is being exported into CSV file to be further processed.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/go_metrics.html

#### Usage

```
usage: go_metrics.py [-h] [-u URL] -o OUTPUT [-d DELAY] [-m MAX_RECORDS]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to get metrics
  -o OUTPUT, --output OUTPUT
                        output file name
  -d DELAY, --delay DELAY
                        Delay in seconds between records
  -m MAX_RECORDS, --max_records MAX_RECORDS
                        max records to export (default=all)
```



### `kafka_lags.py`

Plot graph with Kafka lags with linear regression line added into plot.

Source CSV file is to be retrieved from Grafana.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/kafka_lags.html

#### Usage

```
kafka_lags.py input_file.csv
```

#### Example

```
kafka_lags.py overall.csv
```


------------------------------------------------------------------------------

## Checking tools

These utilities are stored in `checks` subdirectory.

### `json_check.py`

Simple checker if all JSONs have the correct syntax (not scheme).

#### Usage

```
Usage:

```text
usage: json_check.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  make it verbose
  -n, --no-colors  disable color output
  -d DIRECTORY, --directory DIRECTORY
                        directory with JSON files to check
```

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/json_check.html



### `open_api_check.py`

Simple checker for OpenAPI specification files.

#### Usage

```
usage: open_api_check.py [-h] [-v] [-n] [-d DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         make it verbose
  -n, --no-colors       disable color output
  -d DIRECTORY, --directory DIRECTORY
                        directory OpenAPI JSON file to check
```

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/open_api_check.html



## Utilities for logs handling

### `anonymize_aggregator_log.py`

Anonymize aggregator log files by hashing organization ID and cluster ID.
This tool works as a standard Unix filter.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/anonymize_aggregator_log.html

#### Usage:

```
 anonymize_aggregator_log.py [-h] -s SALT

 optional arguments:
   -h, --help            show this help message and exit
   -s SALT, --salt SALT  salt for hashing algorithm
```

### Example:

```
 anonymize_aggregator_log.py -s foobar < original.log > anonymized.log
```


### `anonymize_ccx_pipeline_log.py`

Anonymize CCX data pipeline log files by hashing organization ID and cluster ID.
This tool works as a standard Unix filter.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/anonymize_ccx_pipeline_log.html

#### Usage:

```
 anonymize_ccx_pipeline_log.py [-h] -s SALT < input.log > output.log

 optional arguments:
   -h, --help            show this help message and exit
   -s SALT, --salt SALT  salt for hashing algorithm
```

### Example:

```
 anonymize_ccx_pipeline_log.py -s foobar < original.log > anonymized.log
```

------------------------------------------------------------------------------



## Animations etc.

These utilities are stored in `anim` subdirectory.

That subdirectory contains tools to generate various animations with Insights
Results Aggregator, Insights Content Service, and Insights Results Smart proxy
architecture and data or command flows. Theese tools are invoked from command
line and don't not accept any command line argument (yet).


### `anim_external_data_pipeline.go`

Creates animation based on static GIF image + set of programmed rules. That
animation displays the data flow for the whole external data pipeline.

#### Description

Specialized utility used just to create data flow for the whole external data pipeline.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/anim_external_data_pipeline.html

#### Build

Go version 1.14 or newer is required to build this tool.

```
go build anim_external_data_pipeline.go
```

#### Usage

```
go run anim_external_data_pipeline.go
```

### `anim_aggregator_consumer.go`

Creates animation based on static GIF image + set of programmed rules. That
animation displays the data flow for Insights Results Aggregator consumer
service.

#### Description

Specialized utility used just to create https://github.com/RedHatInsights/insights-results-aggregator/blob/master/docs/assets/anim_aggregator_consumer.gif

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/anim_aggregator_consumer.html

#### Build

Go version 1.14 or newer is required to build this tool.

```
go build anim_aggregator_consumer.go
```

#### Usage

```
go run anim_aggregator_consumer.go
```

------------------------------------------------------------------------------




### `anim_smart_proxy.go`

Creates animation based on static GIF image + set of programmed rules. That
animation displays data flow between Insights Results Smart Proxy and other
services (internal and external ones).

#### Description

Specialized utility used just to create https://redhatinsights.github.io/insights-content-service/architecture/architecture.gif

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/anim_smart_proxy.html

#### Build

Go version 1.14 or newer is required to build this tool.

```
go build anim_smart_proxy.go
```

#### Usage

```
go run anim_smart_proxy.go
```

------------------------------------------------------------------------------



### `insights_operator_pull_only.go`

Creates animation from static GIF image + set of programmed rules.

#### Description

Specialized utility used just to create https://redhatinsights.github.io/insights-results-smart-proxy/io-pulling-only.gif animation

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/insights_operator_pull_only.html

#### Build

Go version 1.14 or newer is required to build this tool.

```
go build insights_operator_pull_only.go
```

#### Usage

```
go run insights_operator_pull_only.go
```

------------------------------------------------------------------------------



### `insights_operator_prometheus.go`

Creates animation based on static GIF image + set of programmed rules. That
animation displays the data flow from Insights Operator to OCP WebConsole
via Prometheus metrics.

#### Description

Specialized utility used just to create https://redhatinsights.github.io/insights-results-smart-proxy/io-pulling-prometheus-anim.gif animation

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/insights_operator_prometheus.html

#### Build

Go version 1.14 or newer is required to build this tool.

```
go build insights_operator_prometheus.go
```

#### Usage

```
go run insights_operator_prometheus.go
```

------------------------------------------------------------------------------



### `insights_operator_to_web_console.go`

Creates animation from static GIF image + set of programmed rules.

#### Description

Specialized utility used just to create https://redhatinsights.github.io/insights-results-smart-proxy/io-pulling-prometheus-anim.gif animation

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/insights_operator_to_web_console.html

#### Build

Go version 1.14 or newer is required to build this tool.

```
go build insights_operator_to_web_console.go
```

#### Usage

```
go run insights_operator_to_web_console.go
```

------------------------------------------------------------------------------



## Other utilities

### `run_pycodestyle.py`

Simple checker of all Python sources in the given directory (usually repository).

#### Description

This script tries to find all files in current directory and subdirectories
with '\*.py' extension.  Then it checks all those files for any style
violations. Each violation is printed and then total errors is displayed as
well.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/run_pycodestyle.html

#### Usage

To check all files in current directory and all subdirectories:

```
python3 run_pycodestyle.py
```

------------------------------------------------------------------------------
## Converters

These utilities are stored in `converters` subdirectory.



### `json2edn.py`

Converts structured data from JSON format into EDN format.

#### Description

Converts structured data from JSON format into EDN format. This script is based
on `edn_format` Python package, that needs to be installed by using `pip` or
`pip3`.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/json2edn.html

#### Usage

```
python3 json2edn.py input.json > output.edn
```


### `edn2json.py`

Converts structured data from EDN format into JSON format.

#### Description

Converts structured data from EDN format into JSON format. This script is based
on `edn_format` Python package, that needs to be installed by using `pip` or
`pip3`.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/edn2json.html

#### Usage

```
python3 edn2json.py input.edn > output.json
```

------------------------------------------------------------------------------

## Testing tools

### `st.py` (Stage Tester)

#### Description

This script can be used to perform several operations with external data
pipeline usually deployed on Stage environment and accessible through proxy
server.

First operation retrieves list of clusters from the external data pipeline
through the standard REST API (and optionally via proxy server). Organization
ID needs to be provided via CLI option, because list of clusters is filtered by
organization. This operation is selected by using `-l` command line option.

Second operation retrieves results from the external data pipeline for several
clusters. List of clusters needs to be stored in a plain text file. Name of
this text file is to be provided by `-i` command line option. This operation is
selected by using `-r` command line option.

Third operation compares two sets of results. Each set needs to be stored in
separate directory. CSV file with detailed comparison of such two sets is
generated during this operation. This operation is selected by using `-c`
command line option.

Fourth operation retrieves processing timestamp for both set of results and
stores these timestamps into CSV files for further analysis.

REST API on Stage environment is accessed through proxy. Proxy name should be
provided via CLI together with user name and password used for basic auth.

#### Usage

```
st.py [-h] [-a ADDRESS] [-x PROXY] [-u USER] [-p PASSWORD]
      [-o ORGANIZATION] [-l] [-r] [-i INPUT] [-c] [-d1 DIRECTORY1]
      [-d2 DIRECTORY2] [-e EXPORT_FILE_NAME] [-d] [-v] [-t]


optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Address of REST API for external data pipeline
  -x PROXY, --proxy PROXY
                        Proxy to be used to access REST API
  -u USER, --user USER  User name for basic authentication
  -p PASSWORD, --password PASSWORD
                        Password for basic authentication
  -o ORGANIZATION, --organization ORGANIZATION
                        Organization ID
  -l, --cluster-list    Operation to retrieve list of clusters via REST API
  -r, --retrieve-results
                        Retrieve results for given list of clusters via REST
                        API
  -t, --export-times    Export processing times to CSV files that can be used
                        for further analysis
  -i INPUT, --input INPUT
                        Specification of input file (with list of clusters,
                        for example)
  -c, --compare-results
                        Compare two sets of results, each set stored in its
                        own directory
  -d1 DIRECTORY1, --directory1 DIRECTORY1
                        First directory containing set of results
  -d2 DIRECTORY2, --directory2 DIRECTORY2
                        Second directory containing set of results
  -e EXPORT_FILE_NAME, --export EXPORT_FILE_NAME
                        Name of CSV file with exported comparison results
  -d, --additional-info
                        Add additional info about data pipeline components
                        into CSV report
  -v, --verbose         Make messages verbose
```

#### Examples

* Retrieve list of clusters via REST API for organization ID 12345678

```
st.py -l -a https://$REST_API_URL -x http://$PROXY_URL -u $USER_NAME -p $PASSWORD -o 12345678
```

* Read results for clusters whose IDs are stored in file named `clusters.txt`

```
st.py -r -a https://$REST_API_URL -x http://$PROXY_URL -u $USER_NAME -p $PASSWORD -i clusters.txt
```

* Export processing timestamps into CSV files

```
st.py -t -d1=c1 -d2=c2
```

* Compare results stored in directories `c1` and `c`, results w/o info about the pipeline

```
st.py -c -d1=c1 -d2=c2
```

* Compare results stored in directories `c1` and `c`, results with info about the pipeline

```
st.py -c -v -d1=c1 -d2=c2 -a https://$REST_API_URL -x http://$PROXY_URL -u $USER_NAME -p $PASSWORD
```


#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/st.html



### `pta.py` (Processing Times Analyser)

#### Description

Script to retrieve and analyze processing times from reports taken from external data pipeline

#### Usage

```
usage: pta.py [-h] -i INPUT_FILE [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input INPUT_FILE
                        Specification of input file (with list of clusters,
                        for example)
  -b BIN_SIZE, --bin-size BIN_SIZE
                        Bin size for histograms
  -v, --verbose         Make messages verbose
```

### Example

```
pta.py -i times.csv -v
```

```
pta.py -i times.csv -v -b 100
```

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/pta.html

------------------------------------------------------------------------------

## Database related tools

### `cleanup_old_results.py`

Prepares script to cleanup old results from database.

#### Description

This script can be used to analyze data exported from `report` table by
the following command typed into PSQL console:

    \copy report to 'reports.csv' csv

Script retrieves all reports older than the specified amount of time represented as days.
Then it creates an SQL script that can be run by administrator against selected database.

#### Generated documentation

* https://redhatinsights.github.io/insights-results-aggregator-utils/packages/cleanup_old_results.html

#### Database connection

Howto connect to PSQL console:

    psql -h host

Password can be retrieved from OpenShift console, for example from:
ccx-data-pipeline-qa/browse/secrets/ccx-data-pipeline-db
ccx-data-pipeline-prod/browse/secrets/ccx-data-pipeline-db

#### Usage

    cleanup_old_results.py offset_in_days input_file.csv > cleanup.sql

#### Example

create a script to cleanup all records older than 90 days

    cleanup_old_results.py 90 report.csv > cleanup.sql


## Package manifest

Package manifest is available at [docs/manifest.txt](docs/manifest.txt).
