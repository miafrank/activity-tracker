import boto3


def get_all_items(activity_table_name):
    response = boto3.client('dynamodb').scan(TableName=activity_table_name)
    items = []
    for item in response['Items']:
        items.append(parse_multi_item_response(item))
    return items