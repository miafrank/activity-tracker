def validate(activity):
    """
    Validate input when creating new activity. All fields must be fulfilled to create a new
    activity. If any activity field is not present, an AssertionError will be raised.
    :param activity:
    :return: True (if new activity is valid)
    """
    assert activity['activity_date'], "activity date cannot be null"
    assert activity['activity_name'], "activity name cannot be null"
    assert activity['activity_duration'], "activity duration cannot be null"

    return True
