from flask import Flask, jsonify, request
from app.dynamodb import dynamodb_utils
from flask_cors import CORS

app = Flask(__name__)
enable_cors_for_all_routes = CORS(app)


@app.route("/activities", methods=['GET'])
def get_all_activities():
    return jsonify(dynamodb_utils.get_all_items())


@app.route('/activities', methods=['POST'])
def create_new_activity():
    return jsonify(id=dynamodb_utils.create_new_item(request.get_json())['id'])


@app.route('/activities/<activity_id>', methods=['GET'])
def get_activity_by_id(activity_id):
    return jsonify(item=dynamodb_utils.get_activity_by_id(activity_id))


@app.route('/activities/<activity_id>', methods=['PUT'])
def update_activity_by_id(activity_id):
    request_data = request.get_json()
    return jsonify(dynamodb_utils.update_item_by_id(activity_id, request_data))


@app.route('/activities/<activity_id>', methods=['DELETE', 'POST'])
def delete_activity_by_id(activity_id):
    return jsonify(item=dynamodb_utils.delete_item_by_id(activity_id))


if __name__ == '__main__':
    app.run(port='5000')
