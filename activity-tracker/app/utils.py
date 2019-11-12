import uuid


def get_row_by_column_name(item):
    return {
        'activity_id': item['id'].get('S'),
        'activity_date': item['activity_date'].get('S'),
        'activity_name': item['activity_name'].get('S'),
        'activity_duration': item['activity_duration'].get('S')
    }


def get_rows(item):
    return {
        'activity_id': item['id'],
        'activity_date': item['activity_date'],
        'activity_name': item['activity_name'],
        'activity_duration': item['activity_duration']
    }


def generate_uuid():
    return str(uuid.uuid4())
