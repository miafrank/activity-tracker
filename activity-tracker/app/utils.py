def get_rows(item):
    return {
        'activity_id': item['id'].get('S'),
        'activity_date': item['activity_date'].get('S'),
        'activity_name': item['activity_name'].get('S'),
        'activity_duration': item['activity_duration'].get('S')
    }