from moto import mock_dynamodb2
import boto3
from app import aws_dynamo_controller


@mock_dynamodb2
def test_save_items():
    mock_dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    mock_table_name = 'mock_activity_table'

    mock_dynamodb_table =\
        mock_dynamodb.create_table(
            TableName=mock_table_name,
            KeySchema=[
                {
                    'AttributeName': 'Duration',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'Activity_Name',
                    'KeyType': 'RANGE'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Activity_Name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Duration',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

    mock_aws_item = {'Duration': 1, 'Activity_Name': 'running'}
    mock_dynamodb_table.put_item(Item=mock_aws_item)

    assert mock_aws_item['Duration'] == 1
    assert mock_aws_item['Activity_Name'] == "running"
