from flask_api import status

import logging

from app import utils
from app.config import ITEM_NOT_FOUND, ITEM_DELETED_SUCCESSFULLY
from app.validator import validate


def get_all_items(client):
    items = [dynamodb_rows_dtype_to_json(item) for item in client['Items']]
    return items


def create_new_item(json, resource):
    if validate(activity=json):
        json['id'] = utils.generate_uuid()
        resource.put_item(Item=json)
    return json


def get_item_by_id(activity_id, resource):
    response = resource.get_item(Key={'id': str(activity_id)})
    if 'Item' in response:
        return dynamodb_rows_to_json(response['Item'])


def update_item_by_id(activity_id, payload, resource):
    activity_by_id = get_item_by_id(activity_id, resource)

    if 'activity_date' not in payload:
        payload['activity_date'] = activity_by_id['activity_date']
    if 'activity_duration' not in payload:
        payload['activity_duration'] = activity_by_id['activity_duration']
    if 'activity_name' not in payload:
        payload['activity_name'] = activity_by_id['activity_name']

    return resource.update_item(
        Key={'id': str(activity_id)},
        UpdateExpression="set activity_date = :date, activity_name= :name, activity_duration = :duration",
        ExpressionAttributeValues={
            ':date': payload['activity_date'],
            ':name': payload['activity_duration'],
            ':duration': payload['activity_name']
        },
        ReturnValues="UPDATED_NEW")


def item_deleted_successfully(response):
    http_response = response['ResponseMetadata']['HTTPStatusCode']
    return ITEM_DELETED_SUCCESSFULLY if http_response == status.HTTP_200_OK else logging.info("Something went wrong")


def delete_item_by_id(activity_id, resource):
    if get_item_by_id(activity_id, resource):
        deleted_item = resource.delete_item(Key={'id': str(activity_id)})
        return item_deleted_successfully(deleted_item)
    else:
        return ITEM_NOT_FOUND


def dynamodb_rows_to_json(item):
    return {
        'activity_id': item['id'],
        'activity_date': item['activity_date'],
        'activity_name': item['activity_name'],
        'activity_duration': item['activity_duration']
    }


def dynamodb_rows_dtype_to_json(item):
    return {
        'activity_id': get_item_field_value(item['id']),
        'activity_date': get_item_field_value(item['activity_date']),
        'activity_name': get_item_field_value(item['activity_name']),
        'activity_duration': get_item_field_value(item['activity_duration'])
    }


def get_item_field_value(field_name):
    return field_name.get('S')