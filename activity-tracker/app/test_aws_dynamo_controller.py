from moto import mock_dynamodb2
import boto3
from app import aws_dynamo_controller


@mock_dynamodb2
def test_save_items():
    mock_aws_item = {"id": "3"}
    # todo when create_item is called it actually calls aws - how to stop that
    aws_dynamo_controller.create_new_item(mock_aws_item)
    assert mock_aws_item['Duration'] == 2
    assert mock_aws_item['Activity_Name'] == "swimming"


@mock_dynamodb2
def dynamodb_setup():
    mock_dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    mock_table_name = 'mock_activity_table'
    mock_dynamodb_table = mock_dynamodb.create_table(
        TableName=mock_table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    return mock_dynamodb_table


@mock_dynamodb2
def test_stack_of():
    table_name = 'mock_activity_table'
    dynamodb = boto3.resource('dynamodb', 'us-east-1')

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    item_id = aws_dynamo_controller.generate_uuid()
    item = {'id': item_id}
    table = dynamodb.Table(table_name)
    aws_dynamo_controller.create_new_item(item, table)
    response = table.get_item(
        Key={
            'id': item_id
        }
    )
    if 'Item' in response:
        item = response['Item']

    assert("id" in item)
    assert (item["id"], item_id)
