import sys
import traceback

from moto import mock_dynamodb2
import boto3
from app import aws_dynamo_controller


table_name = 'mock_activity_table'


@mock_dynamodb2
def dynamodb_setup():
    dynamodb = boto3.resource('dynamodb', 'us-east-1')
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'ZS',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    return dynamodb.Table(table_name)


def create_mock_item(activity_date, activity_name, activity_duration):
    mock_item = {
        'activity_date': activity_date,
        'activity_name': activity_name,
        'activity_duration': activity_duration
    }
    return mock_item


def create_mock_response(activity_date, activity_name, activity_duration, item_id):
    mock_response = {
        'activity_date': activity_date,
        'activity_name': activity_name,
        'activity_duration': activity_duration,
        'id': item_id
    }
    return mock_response


@mock_dynamodb2
def test_create_new_item():
    table = dynamodb_setup()
    item_id = aws_dynamo_controller.generate_uuid()
    mock_item = create_mock_item("04/23/2019", "walking", "3")

    aws_dynamo_controller.create_new_item(mock_item, table)
    mock_response = table.get_item(Key={'id': item_id})

    if 'Item' in mock_response:
        mock_item = mock_response['Item']

    assert ("id" in mock_item)


@mock_dynamodb2
def test_item_by_id():
    table = dynamodb_setup()
    item_id = '123'
    aws_dynamo_controller.get_item_by_id(item_id, table)
    table.get_item(Key={'id': item_id})


@mock_dynamodb2
def test_delete_item_by_id():
    table = dynamodb_setup()
    item_id = 456
    aws_dynamo_controller.delete_item_by_id(item_id, table)
