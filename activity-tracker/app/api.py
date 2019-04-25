from flask import Flask, jsonify, request
from app import aws_dynamo_controller

app = Flask(__name__)


@app.route("/activities", methods=['GET'])
def get_all_items():
    return jsonify(activities=aws_dynamo_controller.get_all_items())


@app.route('/activities', methods=['POST'])
def create_activity():
    request_data = request.get_json()
    activity_id = aws_dynamo_controller.create_new_item(request_data)
    return jsonify(id=activity_id)


@app.route('/activities/<activity_id>', methods=['GET'])
def get_activity_by_id(activity_id):
    item = aws_dynamo_controller.get_item_by_id(activity_id)
    return jsonify(item=item)


@app.route('/activities/<activity_id>', methods=['PUT'])
def update_activity_by_id(activity_id):
    request_data = request.get_json()
    print(request_data)
    update_item = aws_dynamo_controller.update_item_by_id(activity_id, request_data)
    print(update_item)
    return jsonify(update_item)


@app.route('/activities/<activity_id>', methods=['DELETE', 'POST'])
def delete_activity_by_id(activity_id):
    deleted_item = aws_dynamo_controller.delete_item_by_id(activity_id)
    return jsonify(item=deleted_item)


if __name__ == '__main__':
    app.run(port='5000')
