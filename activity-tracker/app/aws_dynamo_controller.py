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
    json['id'] = str(random_uuid)
    activity_table_resource.put_item(Item=json)
    return json['id']


def get_item_by_id(activity_id):
    # todo if id is not found -> send tht back in response to user
    response = activity_table_resource.get_item(
        TableName=activity_table_name,
        Key={'id': str(activity_id)}
    )
    return parse_item_response(response)


def delete_item_by_id(activity_id):
    # todo if id is not found -> send tht back in response to user
    response = activity_table_resource.delete_item(
        TableName=activity_table_name,
        Key={'id': str(activity_id)}
    )
    return response


def update_item_by_id(activity_id, json):
    if 'Date' in json.keys():
        field_name = 'Date'
        date = json['Date']
        item = update_item_fields(date, activity_id, field_name)
        return item
    if 'Activity_Name' in json.keys():
        activity_name = json['Activity_Name']
        item = update_item_fields(activity_name, activity_id)
        return item
    if 'Duration' in json.keys():
        field_name = 'Duration'
        duration = json['Duration']
        item = update_item_fields(duration, activity_id, field_name)
        return item


def update_item_fields(field_value, activity_id, field_name):
    item = activity_table_resource.update_item(
        Key={'id': str(activity_id)},
        # UpdateExpression='set Duration = :a',
        UpdateExpression='set ' + field_name + '= :a',
        ExpressionAttributeValues={
            ':a': field_value,
        },
        ReturnValues="UPDATED_NEW"
    )
    return item


def parse_item_response(item_response):
    item = item_response['Item']
    date = item['activity_date']
    activity_name = item['activity_name']
    activity_id = str(item['id'])
    duration = str(item['activity_duration'])

    item_as_dict = {
            'id': activity_id,
            'activity_date': date,
            'activity_name': activity_name,
            'activity_duration': duration
            }

    return item_as_dict
