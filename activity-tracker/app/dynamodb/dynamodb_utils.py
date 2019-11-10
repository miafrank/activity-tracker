from . import dynamodb_resource_service
from app import utils

dynamodb_client = dynamodb_resource_service.dynamodb_client()
dynamodb_resource = dynamodb_resource_service.dynamodb_resource()


def get_all_items():
    items = [utils.get_rows(item) for item in dynamodb_client['Items']]
    return items


def create_new_item(json):
    json['id'] = utils.generate_uuid()
    dynamodb_resource.put_item(Item=json)
    return json
