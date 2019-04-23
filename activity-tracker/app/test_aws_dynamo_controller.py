import pytest
from moto import mock_dynamodb
import boto3


def test_save_items():
    mock_dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    mock_dynamodb.create_table(TableName='mock_activity_table')

