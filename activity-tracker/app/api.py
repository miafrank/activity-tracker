from flask import Flask, jsonify, request
from app import aws_dynamo_controller

app = Flask(__name__)

# todo update endpoint names to fit rest conventions


@app.route("/activity", methods=['GET'])
def get_all_items():
    return jsonify(aws_dynamo_controller.get_all_items())


@app.route('/create-activity', methods=['POST'])
def create_activity():
    request_data = request.get_json()
    activity_id = aws_dynamo_controller.create_new_item(request_data)
    return jsonify(id=activity_id)


@app.route('/get_activity_by_id/<activity_id>', methods=['GET'])
def get_activity_by_id(activity_id):
    item = aws_dynamo_controller.get_item_by_id(activity_id)
    return jsonify(item)


@app.route('/update-by-id/<activity_id>', methods=['PUT'])
def update_activity_by_id(activity_id):
    request_data = request.get_json()
    update_item = aws_dynamo_controller.update_item_by_id(activity_id, request_data)
    return jsonify(update_item)


@app.route('/delete-by-id/<activity_id>', methods=['DELETE', 'POST'])
def delete_activity_by_id(activity_id):
    deleted_item = aws_dynamo_controller.delete_item_by_id(activity_id)
    return jsonify(deleted_item)


if __name__ == '__main__':
    app.run(port='8080')
