import boto3
import uuid

from boto3.dynamodb.conditions import Attr
from flask_api import status

ITEM_NOT_FOUND = "item not found"
ITEM_DELETED_SUCCESSFULLY = "item deleted successfully"


def generate_uuid():
    random_uuid = uuid.uuid4()
    return str(random_uuid)


def get_all_items(activity_table_name):
    response = boto3.client('dynamodb').scan(TableName=activity_table_name)
    items = []
    for item in response['Items']:
        items.append(parse_multi_item_response(item))
    return items


def create_new_item(json, resource):
    json['id'] = generate_uuid()
    resource.put_item(Item=json)
    return json['id']


def get_item_by_id(activity_id, resource, table_name):
    response = get_item_by_table_name_and_key(activity_id, resource, table_name)
    if 'Item' in response.keys():
        return parse_item_response(response)
    return ITEM_NOT_FOUND


def get_item_by_table_name_and_key(activity_id, resource, table_name):
    response = resource.get_item(
        TableName=table_name,
        Key={'id': str(activity_id)}
    )
    return response


def delete_item_by_id(activity_id, resource, activity_table_name):
    item_exists_in_table = get_item_by_table_name_and_key(activity_id, resource, activity_table_name)

    if 'Item' in item_exists_in_table.keys():
        response = resource.delete_item(
            TableName=activity_table_name,
            Key={'id': str(activity_id)}
        )
        return item_deleted_successfully(response)
    else:
        return ITEM_NOT_FOUND


def item_deleted_successfully(response):
    response_meta = response['ResponseMetadata']
    http_status = response_meta['HTTPStatusCode']

    if http_status == status.HTTP_200_OK:
        return ITEM_DELETED_SUCCESSFULLY


# todo update method to update all fields at once + response from query only returns first field that is updated
def update_item_by_id(activity_id, json, resource):
    activity_date = 'activity_date'
    activity_name = 'activity_name'
    activity_duration = 'activity_duration'

    if len(json) > 0 and activity_date in json.keys():
        return update_activity_date(activity_id, json, resource)
    if len(json) > 0 and activity_name in json.keys():
        return update_activity_name(activity_id, json, resource)
    if len(json) > 0 and activity_duration in json.keys():
        return update_activity_duration(activity_id, json, resource)


def update_activity_duration(activity_id, json, resource):
    field_name = 'activity_duration'
    activity_duration_value = json['activity_duration']
    return update_item_fields(activity_id, activity_duration_value, field_name, resource)


def update_activity_name(activity_id, json, resource):
    field_name = 'activity_name'
    activity_name_value = json['activity_name']
    return update_item_fields(activity_id, activity_name_value, field_name, resource)


def update_activity_date(activity_id, json, resource):
    field_name = 'activity_date'
    activity_date_value = json['activity_date']
    return update_item_fields(activity_id, activity_date_value, field_name, resource)


def update_item_fields(activity_id, field_value, field_name, resource):
    item = resource.update_item(
        Key={'id': str(activity_id)},
        UpdateExpression='set ' + field_name + '= :a',
        ExpressionAttributeValues={
            ':a': field_value,
        },
        ReturnValues="UPDATED_NEW"
    )
    return item


def query_by_activity(json, resource):
    activity_name = json['activity_name']
    response = resource.scan(
        FilterExpression=Attr('activity_name').eq(activity_name)
    )
    items = []
    for item in response['Items']:
        items.append(parse_single_item_response(item))
    return items


# todo look into filtering - takes into account month and day but not year
def query_by_date(json, resource):
    start_date = json['start_date']
    end_date = json['end_date']
    response = resource.scan(
        FilterExpression=Attr('activity_date').between(start_date, end_date)
    )
    items = []
    for item in response['Items']:
        items.append(parse_single_item_response(item))
    return items


def parse_item_response(item_response):
    item = item_response['Item']
    item_dict = parse_single_item_response(item)
    return item_dict


def parse_single_item_response(item):
    activity_id = item['id']
    activity_date = item['activity_date']
    activity_name = item['activity_name']
    activity_duration = item['activity_duration']

    return item_response_as_dict(activity_date, activity_duration, activity_id, activity_name)


def parse_multi_item_response(item):
    activity_id = get_item_field_value(item['id'])
    activity_date = get_item_field_value(item['activity_date'])
    activity_name = get_item_field_value(item['activity_name'])
    activity_duration = get_item_field_value(item['activity_duration'])

    item_dict = item_response_as_dict(activity_date, activity_duration, activity_id, activity_name)
    return item_dict


def item_response_as_dict(activity_date, activity_duration, activity_id, activity_name):
    item_dict = {
        'activity_id': activity_id,
        'activity_date': activity_date,
        'activity_name': activity_name,
        'activity_duration': activity_duration
    }
    return item_dict


def get_item_field_value(field_name):
    return field_name.get('S')
