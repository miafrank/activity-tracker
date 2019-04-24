#!/usr/bin/env bash
aws dynamodb create-table --table-name activity \
--key-schema AttributeName=Id,KeyType=HASH \
--attribute-definitions \
AttributeName=Id,AttributeType=S \
--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1