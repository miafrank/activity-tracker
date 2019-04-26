import boto3
import uuid

ITEM_NOT_FOUND = "item not found"
activity_table_name = 'activity'


def generate_uuid():
    random_uuid = uuid.uuid4()
    return str(random_uuid)


def get_all_items():
    response = boto3.client('dynamodb').scan(TableName=activity_table_name)
    # todo clean up item response
    return response['Items']


def create_new_item(json, resource):
    json['id'] = generate_uuid()
    resource.put_item(Item=json)
    return json['id']


def get_item_by_id(activity_id, resource):
    response = resource.get_item(
        TableName=activity_table_name,
        Key={'id': str(activity_id)}
    )
    if 'Item' in response.keys():
        return parse_item_response(response)
    return ITEM_NOT_FOUND


def delete_item_by_id(activity_id, resource):
    response = resource.delete_item(
        TableName=activity_table_name,
        Key={'id': str(activity_id)}
    )
    if 'Item' in response.keys():
        return parse_item_response(response)
    return ITEM_NOT_FOUND


def item_exists(response):
    if 'Item' in response.keys():
        return parse_item_response(response)


# todo update method to update all fields at once, response from query only
# returns first field that is updated
def update_item_by_id(activity_id, json, resource):
    item = update_activity_date(activity_id, json, resource)
    item = update_activity_name(activity_id, item, json, resource)
    item = update_activity_duration(activity_id, item, json, resource)
    return item


def update_activity_duration(activity_id, item, json, resource):
    if 'activity_duration' in json.keys():
        field_name = 'activity_duration'
        activity_duration_value = json['activity_duration']
        item = update_item_fields(activity_id, activity_duration_value, field_name, resource)
    return item


def update_activity_name(activity_id, item, json, resource):
    if 'activity_name' in json.keys():
        field_name = 'activity_name'
        activity_name_value = json['activity_name']
        item = update_item_fields(activity_id, activity_name_value, field_name, resource)
    return item


def update_activity_date(activity_id, json, resource):
    if 'activity_date' in json.keys():
        field_name = 'activity_date'
        activity_date_value = json['activity_date']
        item = update_item_fields(activity_id, activity_date_value, field_name, resource)
    return item


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
