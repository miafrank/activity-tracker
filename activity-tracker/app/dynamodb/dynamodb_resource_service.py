import boto3

from app.config import ACTIVITY_TABLE_NAME


def dynamodb_client():
    return boto3.client('dynamodb').scan(TableName=ACTIVITY_TABLE_NAME)


def dynamodb_resource():
    return boto3.resource('dynamodb').Table(ACTIVITY_TABLE_NAME)
