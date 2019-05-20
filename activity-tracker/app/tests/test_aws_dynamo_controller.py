import boto3
from moto import mock_dynamodb2
from app.dynamodb import aws_dynamo_controller
import pytest


table_name = 'mock_activity_table'


@mock_dynamodb2
def dynamodb_setup():
    dynamodb = boto3.resource('dynamodb', 'us-east-1')
    dynamodb.create_table(
        TableName=table_name,
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
    table = dynamodb.Table(table_name)
    return table


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
    table = dynamodb_setup()
    item_id = aws_dynamo_controller.generate_uuid()
    mock_item = create_mock_item("04/23/2019", "walking", "3")

    aws_dynamo_controller.create_new_item(mock_item, table)
    mock_response = table.get_item(Key={'id': item_id})

    if 'Item' in mock_response:
        mock_item = mock_response['Item']

    assert ("id" in mock_item)


@mock_dynamodb2
def test_get_item_by_id():
    table = dynamodb_setup()
    item_id = "123"
    table.put_item(
        Item={
            'activity_date': "02/09/2222",
            'activity_name': "hang gliding",
            'activity_duration': "50",
            'id': item_id
        }
    )
    mock_item = aws_dynamo_controller.get_item_by_id(item_id, table, table_name)

    assert mock_item['activity_id'] == "123"
    assert mock_item['activity_duration'] == "50"


@mock_dynamodb2
def test_delete_item_by_id():
    table = dynamodb_setup()
    item_id = "456"
    table.put_item(
        Item={
            "activity_date": "04/17/2019",
            "activity_duration": "1",
            "id": item_id,
            'activity_name': 'running'
        })
    deleted_item = aws_dynamo_controller.delete_item_by_id(item_id, table, table_name)

    assert deleted_item == "item deleted successfully"


@mock_dynamodb2
def test_delete_item_by_id_where_id_not_found_in_db():
    table = dynamodb_setup()
    deleted_item = aws_dynamo_controller.delete_item_by_id("222", table, table_name)
    assert deleted_item == "item not found"


@mock_dynamodb2
def test_update_item_by_id():
    table = dynamodb_setup()
    item_id = "555"
    mock_json_before_update = create_mock_response("02/18/2019", "walking", "1", "555")
    mock_json_after_update = create_mock_response("01/28/2019", "running", "2", "568")

    aws_dynamo_controller.update_item_by_id(item_id, mock_json_after_update, table)

    assert mock_json_before_update['activity_date'] != mock_json_after_update['activity_date']
    assert mock_json_before_update['activity_duration'] != mock_json_after_update['activity_duration']
    assert mock_json_before_update['activity_name'] != mock_json_after_update['activity_name']


@mock_dynamodb2
def test_query_by_activity():
    table = dynamodb_setup()
    activity_name_json = {'activity_name': 'running'}

    table.put_item(
        Item={
            "activity_date": "04/17/2019",
            "activity_duration": "1",
            "id": "de33dfef-e157-48a2-b6d9-fa28caf4db99",
            'activity_name': 'running'
        })

    table.put_item(
        Item={
            "activity_date": "04/30/2019",
            "activity_duration": "1",
            "id": "c727f0c6-08ad-4311-a358-5ad4ae2fbc19",
            "activity_name": "running"
        })

    table.put_item(
        Item={
            "activity_date": "06/30/2019",
            "activity_duration": "1",
            "id": "c727f0c6-08ad-4311-9999-5ad4ae2fbc19",
            "activity_name": "swimming"
        })

    items = aws_dynamo_controller.query_by_activity(activity_name_json, table)

    assert items[0].get('activity_id') == "de33dfef-e157-48a2-b6d9-fa28caf4db99"
    assert items[1].get('activity_id') == "c727f0c6-08ad-4311-a358-5ad4ae2fbc19"
    assert 'running' in items[0].get('activity_name')
    assert len(items) == 2


@mock_dynamodb2
# fixme test failing in filter by date
def test_query_by_date():
    table = dynamodb_setup()
    activity_start_and_end_dates = {"start_date": "04012019", "end_date": "04152019"}

    item_within_date_range = table.put_item(
        Item={
            "activity_date": "04/17/2019",
            "activity_duration": "1",
            "id": "de33dfef-e157-48a2-b6d9-fa28caf4db99",
            "activity_name": "running"
        })

    item_out_of_date_range = table.put_item(
        Item={
            "activity_date": "04/30/2019",
            "activity_duration": "1",
            "id": "c727f0c6-08ad-4311-a358-5ad4ae2fbc19",
            "activity_name": "running"
        })

    items = aws_dynamo_controller.query_by_date(activity_start_and_end_dates, table)
    assert item_within_date_range == items
    assert item_out_of_date_range not in items
    assert len(items) == 1
