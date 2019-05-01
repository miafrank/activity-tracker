from flask import Flask, jsonify, request
from app.dynamodb import aws_dynamo_controller
from app.dynamodb import dynamodb_resource

application = Flask(__name__)
activity_table_name = 'activity'


@application.route("/activities", methods=['GET'])
def get_all_items():
    return jsonify(activities=aws_dynamo_controller.get_all_items(activity_table_name))


@application.route('/activities', methods=['POST'])
def create_activity():
    request_data = request.get_json()
    activity_id = aws_dynamo_controller.create_new_item(request_data, dynamodb_resource.set_up_resource())
    return jsonify(id=activity_id)


@application.route('/activities/<activity_id>', methods=['GET'])
def get_activity_by_id(activity_id):
    item = aws_dynamo_controller.get_item_by_id(activity_id, dynamodb_resource.set_up_resource(), activity_table_name)
    return jsonify(item=item)


@application.route('/activities/<activity_id>', methods=['PUT'])
def update_activity_by_id(activity_id):
    request_data = request.get_json()
    update_item = \
        aws_dynamo_controller.update_item_by_id(
            activity_id,
            request_data,
            dynamodb_resource.set_up_resource())

    return jsonify(update_item)


@application.route('/activities/<activity_id>', methods=['DELETE', 'POST'])
def delete_activity_by_id(activity_id):
    deleted_item = aws_dynamo_controller.delete_item_by_id(activity_id, dynamodb_resource.set_up_resource(),
                                                           activity_table_name)
    return jsonify(item=deleted_item)


if __name__ == '__main__':
    application.run(port='5000')
