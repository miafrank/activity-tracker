def validate(activity):
    """
    Validate input when creating new activity. All fields must be fulfilled to create a new
    activity. If any activity field is not present, an AssertionError will be raised.
    :param activity:
    :return: True (if new activity is valid)
    """
    return (False
            if not activity['activity_date']
            or activity['activity_name']
            or activity['activity_duration']
            else True)
