#!/bin/bash

export S3_ENDPOINT_URL="http://localhost:4566"

docker compose up -d 

sleep 1

aws --endpoint-url=http://localhost:4566 \
s3 mb s3://nyc-duration

pipenv run python integration_test.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then 
    docker compose logs
    docker compose down
    echo "Test Failed!"
    echo "Debug from the log"
    exit ${ERROR_CODE}
fi

docker compose down

echo "Test Passed!!!"
echo "Congratulation"