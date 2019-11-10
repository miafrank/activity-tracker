import boto3

from app.config import ACTIVITY_TABLE_NAME


def activity_table_resource():
    return boto3.client('dynamodb').scan(TableName=ACTIVITY_TABLE_NAME)
