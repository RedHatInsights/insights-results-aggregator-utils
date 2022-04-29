#!/bin/bash

export GEVENT_SUPPORT=True
export OFFLINE_TOKEN=..
export LOGIN_URL=..
export CLIENT_ID=rhsm-api
export API_URL=https://console.redhat.com
export ORGANIZATION=..
export LOG_LEVEL=ERROR
export USERS_NO=10

export ACCESS_TOKEN=$(curl $LOGIN_URL -d grant_type=refresh_token -d client_id=$CLIENT_ID -d refresh_token=$OFFLINE_TOKEN | jq --raw-output .access_token)

cd stage_tester

python st.py -l -a $API_URL -p $ACCESS_TOKEN -o $ORGANIZATION > clusters.txt
python st.py -r -a $API_URL -p $ACCESS_TOKEN -o $ORGANIZATION -i clusters.txt
python st.py -t -d1=.
# python pta.py -i times.csv -v
locust --headless -t 1m --users $USERS_NO --spawn-rate 1 --csv locust --only-summary --host $API_URL --loglevel $LOG_LEVEL