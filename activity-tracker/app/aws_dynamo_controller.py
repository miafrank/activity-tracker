import boto3
import uuid

dynamodb_resource = boto3.resource('dynamodb')
activity_table_name = 'activity'
activity_table_resource = dynamodb_resource.Table(activity_table_name)
dynamodb_client = boto3.client('dynamodb')


def get_all_items():
    response = dynamodb_client.scan(TableName=activity_table_name)
    # todo clean up item response
    return response['Items']


def create_new_item(json):
    random_uuid = uuid.uuid4()
    json['Id'] = str(random_uuid)
    return activity_table_resource.put_item(Item=json)


def get_item_by_id(activity_id):
    # todo if id is not found -> send tht back in response to user
    response = activity_table_resource.get_item(
        TableName=activity_table_name,
        Key={'Id': str(activity_id)}
    )
    return parse_item_response(response)


def delete_item_by_id(activity_id):
    # todo if id is not found -> send tht back in response to user
    response = activity_table_resource.delete_item(
        TableName=activity_table_name,
        Key={'Id': str(activity_id)}
    )
    return response


def update_item_by_id(activity_id, json):

    if 'Date' in json.keys():
        date = json['Date']
    if 'Activity_Name' in json.keys():
        activity_name = json['Activity_Name']
    if 'Duration' in json.keys():
        duration = json['Duration']
    item = update_item_fields(date, activity_name, duration, activity_id)

    return item


def update_item_fields(date, activity_name, duration, activity_id):
    item = activity_table_resource.update_item(
        Key={'Id': str(activity_id)},
        UpdateExpression='set Activity_Name = :a, Date = :d, Duration = :u',
        ExpressionAttributeValues={
            ':a': activity_name,
            ':d': date,
            ':u': duration
        },
        ReturnValues="UPDATED_NEW"
    )
    return item


def parse_item_response(item_response):
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
