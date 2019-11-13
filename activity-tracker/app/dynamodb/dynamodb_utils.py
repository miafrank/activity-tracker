from flask_api import status

import logging

from . import dynamodb_resource_service
from app import utils
from app.config import ITEM_NOT_FOUND, ITEM_DELETED_SUCCESSFULLY

dynamodb_client = dynamodb_resource_service.dynamodb_client()
dynamodb_resource = dynamodb_resource_service.dynamodb_resource()


def get_all_items():
    items = [utils.get_rows(item) for item in dynamodb_client['Items']]
    return items


def create_new_item(json):
    json['id'] = utils.generate_uuid()
    dynamodb_resource.put_item(Item=json)
    return json


def get_item_by_id(activity_id):
    response = dynamodb_resource.get_item(Key={'id': str(activity_id)})
    return response


def get_activity_by_id(activity_id):
    response = get_item_by_id(activity_id)
    return utils.get_rows(response['Item']) if 'Item' in response.keys() else ITEM_NOT_FOUND


def update_item_by_id(activity_id, payload):
    # TODO - this is gross but if all values are not passed update expression, exception is raised.
    # it is kind of a hassle to update one by one, so for now i am parsing the json so that all values
    # in expression update are passed to satisfy boto3
    activity_date, activity_duration, activity_name = (payload['activity_date'],
                                                       payload['activity_name'],
                                                       payload['activity_duration'])
    return dynamodb_resource.update_item(
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


def delete_item_by_id(activity_id):
    if get_activity_by_id(activity_id):
        deleted_item = dynamodb_resource.delete_item(Key={'id': str(activity_id)})
        return item_deleted_successfully(deleted_item)
