import boto3

dynamodb = 'dynamodb'
dynamodb_resource = boto3.resource(dynamodb)
dynamodb_client = boto3.client(dynamodb)
activity_table_name = 'activity'


def get_items():
    return dynamodb_client.scan(TableName=activity_table_name)
