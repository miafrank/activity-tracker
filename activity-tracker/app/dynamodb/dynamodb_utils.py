from . import table_resource
from app import utils

dynamodb_client = table_resource.activity_table_resource()


def get_all_items():
    items = [utils.get_rows(item) for item in dynamodb_client['Items']]
    return items
