import boto3
import uuid

ITEM_NOT_FOUND = "item not found"
ITEM_DELETED_SUCCESSFULLY = "item deleted successfully"
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
    response = get_item_by_table_name_and_key(activity_id, resource)
    if 'Item' in response.keys():
        return parse_item_response(response)
    return ITEM_NOT_FOUND


def get_item_by_table_name_and_key(activity_id, resource):
    response = resource.get_item(
        TableName=activity_table_name,
        Key={'id': str(activity_id)}
    )
    return response


def delete_item_by_id(activity_id, resource):
    item_exists_in_table = get_item_by_table_name_and_key(activity_id, resource)
    print(type(item_exists_in_table))

    if 'Item' in item_exists_in_table.keys():
        response = resource.delete_item(
            TableName=activity_table_name,
            Key={'id': str(activity_id)}
        )
        return is_item_deleted_successfully(response)
    else:
        return ITEM_NOT_FOUND


def is_item_deleted_successfully(response):
    response_meta = response['ResponseMetadata']
    http_status = response_meta['HTTPStatusCode']
    OK = 200

    # todo use http status code lib
    if http_status == OK:
        return ITEM_DELETED_SUCCESSFULLY


# todo update method to update all fields at once, response from query only
# returns first field that is updated
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


def parse_item_response(item_response):
    item = item_response['Item']
    date = item['activity_date']
    activity_name = item['activity_name']
    activity_id = str(item['id'])
    duration = str(item['activity_duration'])

    item_dict = item_as_dict(activity_id, activity_name, date, duration)

    return item_dict


def item_as_dict(activity_id, activity_name, date, duration):
    item = {
        'id': activity_id,
        'activity_date': date,
        'activity_name': activity_name,
        'activity_duration': duration
    }
    return item
