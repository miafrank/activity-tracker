import boto3
from moto import mock_dynamodb2

from app.dynamodb import dynamodb_utils
from app.config import ITEM_NOT_FOUND

@mock_dynamodb2
def dynamodb_setup():
    dynamodb = boto3.resource('dynamodb', 'us-east-1')
    dynamodb.create_table(
        TableName='mock_activity_table',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    return dynamodb.Table('mock_activity_table')


def create_mock_item(activity_date, activity_name, activity_duration):
    mock_item = {
        'activity_date': activity_date,
        'activity_name': activity_name,
        'activity_duration': activity_duration
    }
    return mock_item


def create_mock_response(activity_date, activity_name, activity_duration, item_id):
    mock_response = {
        'activity_date': activity_date,
        'activity_name': activity_name,
        'activity_duration': activity_duration,
        'id': item_id
    }
    return mock_response


@mock_dynamodb2
def test_create_new_item():
    mock_item = create_mock_item('04/23/2019', 'walking', '3')

    row = dynamodb_utils.create_new_item(mock_item, dynamodb_setup())

    assert 'id' in row
    

@mock_dynamodb2
def test_get_item_by_id():
    table = dynamodb_setup()
    activity = create_mock_item('02/09/2222', 'hang gliding', '50')
    activity['id'] = '123'
    table.put_item(Item=activity)

    mock_item = dynamodb_utils.get_item_by_id(activity['id'], table)

    assert mock_item['activity_id'] == '123'
    assert mock_item['activity_duration'] == '50'


@mock_dynamodb2
def test_delete_item_by_id():
    table = dynamodb_setup()
    activity = create_mock_item('04/17/2019', '1', 'running')
    activity['id'] = '456'
    table.put_item(Item=activity)

    deleted_item = dynamodb_utils.delete_item_by_id(activity['id'], table)

    assert deleted_item == 'item deleted successfully'


@mock_dynamodb2
def test_delete_item_by_id_where_id_not_found_in_db():
    deleted_item = dynamodb_utils.delete_item_by_id('222', dynamodb_setup())

    assert deleted_item == ITEM_NOT_FOUND


@mock_dynamodb2
def test_update_item_by_id():
    mock_json_before_update = create_mock_response('02/18/2019', 'walking', '1', '555')
    mock_json_after_update = create_mock_response('01/28/2019', 'running', '2', '568')

    dynamodb_utils.update_item_by_id(mock_json_before_update['id'], mock_json_after_update, dynamodb_setup())

    assert mock_json_before_update['activity_date'] != mock_json_after_update['activity_date']
    assert mock_json_before_update['activity_duration'] != mock_json_after_update['activity_duration']
    assert mock_json_before_update['activity_name'] != mock_json_after_update['activity_name']