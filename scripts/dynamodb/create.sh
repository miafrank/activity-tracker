#!/usr/bin/env bash
aws dynamodb create-table --table-name activity \
--key-schema AttributeName=id,KeyType=HASH \
--attribute-definitions \
AttributeName=id,AttributeType=S \
--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1