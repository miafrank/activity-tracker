import boto3


def set_up_resource():
    activity_table_name = 'activity'
    dynamodb_resource = boto3.resource('dynamodb')
    activity_table_resource = dynamodb_resource.Table(activity_table_name)
    return activity_table_resource
