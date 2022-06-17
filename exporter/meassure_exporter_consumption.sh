#!/bin/bash

RESULTS_CSV_PATH="results.csv"
EXPORTER_PATH="../../insights-results-aggregator-exporter"
RULE_HITS_PER_MESSAGE=5

if test -f "$RESULTS_CSV_PATH"; then
    echo "$RESULTS_CSV_PATH exists."
else
    echo "$RESULTS_CSV_PATH doesn't exist. Creating stucture. . ."
    echo "rule_hits_records,reports,recommendations,memory_consumption" > $RESULTS_CSV_PATH
fi

rule_hits_records=0
reports_records=0
recommendations_records=0
total_messages=0

function measure_usage() {
    rm -r output/*.json
    total_messages=$(($total_messages + n_messages))

    # Generate N messages
    echo "Generating $n_messages messages . . ."
    python3 ../input/gen_messages.py -o output/generated_{}.json -r "$n_messages" -g -a -c

    # Send the messages to Kafka
    echo "Sending the $n_messages messages to Kafka . . ."
    ../input/produce.sh

    rule_hits_records=$(($total_messages * $RULE_HITS_PER_MESSAGE))
    echo "Current rule hits should be $rule_hits_records"
    reports_records=$(($total_messages))
    echo "Current reports should be $reports_records"
    recommendations_records=$(($total_messages * $RULE_HITS_PER_MESSAGE))
    echo "Current recommendations should be $recommendations_records"

    # Wait for all the messages to be consumed (manual input)
    read  -n 1 -p "Please, press any key once the aggregator db writer has finished reading the Kafka messages (i.e no activity in logs)"

    tmp_output=$(mktemp)
    (
        cd "$EXPORTER_PATH"
        /usr/bin/time -f "%P %M" "./insights-results-aggregator-exporter" -metadata > /dev/null 2> "$tmp_output"
    )

    memory_consumption=$(cat $tmp_output | tail -n 1 | awk 'NF>1{print $NF}')
    echo "memory consumption is $memory_consumption KB"

    echo "$rule_hits_records,$reports_records,$recommendations_records,$memory_consumption" >> $RESULTS_CSV_PATH
}

for n_messages in {0..10000..1000}
do
    measure_usage
done


# Pretty print the CSV
cat $RESULTS_CSV_PATH | column -t -s,