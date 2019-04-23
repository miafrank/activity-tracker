import boto3

dynamodb_resource = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')
activity_table_name = 'activity'
table_resource = dynamodb_resource.Table(activity_table_name)


def get_items():
    return dynamodb_client.scan(TableName=activity_table_name)


def create_item(json):
    return table_resource.put_item(Item=json)
