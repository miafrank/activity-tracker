from moto import mock_dynamodb2
import boto3
from app import aws_dynamo_controller


@mock_dynamodb2
def dynamodb_setup():
    table_name = 'mock_activity_table'
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
                'AttributeName': 'id',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    return dynamodb.Table(table_name)


@mock_dynamodb2
def test_save_items():
    mock_aws_item = {"id": "3"}
    # todo when create_item is called it actually calls aws - how to stop that
    aws_dynamo_controller.create_new_item(mock_aws_item)
    assert mock_aws_item['Duration'] == 2
    assert mock_aws_item['Activity_Name'] == "swimming"


@mock_dynamodb2
def test_item_in_aws_item():
    table = dynamodb_setup()
    item_id = aws_dynamo_controller.generate_uuid()
    mock_item = {
        'activity_date': "04/23/2019",
        'activity_name': "walking",
        'activity_duration': "3"
    }

    aws_dynamo_controller.create_new_item(mock_item, table)
    response = table.get_item(Key={'id': item_id})

    # todo assert that item generated is in response

    if 'Item' in response:
        mock_item = response['Item']

    assert ("id" in mock_item)
    assert (mock_item["id"], item_id)
