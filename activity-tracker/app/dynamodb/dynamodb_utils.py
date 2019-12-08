from flask_api import status

import logging

from app import utils
from app.config import ITEM_NOT_FOUND, ITEM_DELETED_SUCCESSFULLY, VALIDATION_ERROR
from app.validator import validate


def get_all_items(client):
    items = [dynamodb_rows_to_json(item) for item in client['Items']]
    return items


def create_new_item(json, resource):
    # todo validation fails if input is not valid but the message is not user friendly.
    if validate(activity=json):
        json['id'] = utils.generate_uuid()
        resource.put_item(Item=json)
    return json


def get_item_by_id(activity_id, resource):
    response = resource.get_item(Key={'id': str(activity_id)})
    if 'Item' in response:
        return dynamodb_rows_to_json(response['Item'])


def update_item_by_id(activity_id, payload, resource):
    # TODO - this is gross but if all values are not passed update expression, exception is raised.
    # it is kind of a hassle to update one by one, so for now i am parsing the json so that all values
    # in expression update are passed to satisfy boto3
    activity_date, activity_duration, activity_name = (payload['activity_date'],
                                                       payload['activity_name'],
                                                       payload['activity_duration'])
    return resource.update_item(
        Key={'id': str(activity_id)},
        UpdateExpression="set activity_date = :date, activity_name= :name, activity_duration = :duration",
        ExpressionAttributeValues={
            ':date': activity_date,
            ':name': activity_name,
            ':duration': activity_duration
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
