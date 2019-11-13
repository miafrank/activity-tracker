import uuid


def get_rows(item):
    return {
        'activity_id': item['id'],
        'activity_date': item['activity_date'],
        'activity_name': item['activity_name'],
        'activity_duration': item['activity_duration']
    }


def generate_uuid():
    """
    :return: uuid as str
    """
    return str(uuid.uuid4())
