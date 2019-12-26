def validate(activity):
    """
    Validate input when creating new activity. All fields must be fulfilled to create a new
    activity. If any activity field is not present, method will return False.
    :param activity:
    :return: True (if activity is valid) False (if activity is invalid)
    """
    return (False
            if not activity['activity_date']
            or not activity['activity_name']
            or not activity['activity_duration']
            else True)
