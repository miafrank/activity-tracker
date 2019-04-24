import boto3

dynamodb_resource = boto3.resource('dynamodb')
activity_table_name = 'activity'
activity_table_resource = dynamodb_resource.Table(activity_table_name)
dynamodb_client = boto3.client('dynamodb')


def get_items():
    return dynamodb_client.scan(TableName=activity_table_name)


def create_item(json):
    return activity_table_resource.put_item(Item=json)


def get_item_by_id(activity_id):
    response = activity_table_resource.get_item(
        TableName=activity_table_name,
        Key={'Id': int(activity_id)}
    )
    return parse_item(response)


def parse_item(item_response):
    item = item_response['Item']
    date = item['Date']
    activity_name = item['Activity_Name']
    activity_id = str(item['Id'])
    duration = str(item['Duration'])

    item_as_dict = {
            'Id': activity_id,
            'Date': date,
            'Activity_Name': activity_name,
            'Duration': duration
            }

    return item_as_dict
