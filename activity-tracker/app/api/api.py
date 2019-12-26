from flask import Flask, jsonify, request

from app.api.errors import BadRequest
from app.dynamodb import dynamodb_utils
from app.dynamodb.dynamodb_resource_service import dynamodb_client
from app.dynamodb.dynamodb_resource_service import dynamodb_resource
from flask_cors import CORS

app = Flask(__name__)
enable_cors_for_all_routes = CORS(app)


@app.route("/activities", methods=['GET'])
def get_all_activities():
    return jsonify(activities=dynamodb_utils.get_all_items(dynamodb_client()))


@app.route('/activities', methods=['POST'])
def create_new_activity():
    if not all(request.get_json().values()):
        raise BadRequest('All fields are required to create a new activity', 400)
    return jsonify(dynamodb_utils.create_new_item(request.get_json(), dynamodb_resource()))


@app.route('/activities/<activity_id>', methods=['GET'])
def get_activity_by_id(activity_id):
    return jsonify(item=dynamodb_utils.get_item_by_id(activity_id, dynamodb_resource()))


@app.route('/activities/<activity_id>', methods=['PUT'])
def update_activity_by_id(activity_id):
    return jsonify(dynamodb_utils.update_item_by_id(activity_id, request.get_json(), dynamodb_resource()))


@app.route('/activities/<activity_id>', methods=['DELETE', 'POST'])
def delete_activity_by_id(activity_id):
    return jsonify(item=dynamodb_utils.delete_item_by_id(activity_id, dynamodb_resource()))


@app.errorhandler(BadRequest)
def handle_bad_requests(error):
    payload = dict(error.payload or ())
    payload['status'] = error.status
    payload['message'] = error.message
    return jsonify(payload), 400


if __name__ == '__main__':
    app.run(port='5000')
