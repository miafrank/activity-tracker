from flask import Flask, jsonify, request
from app.dynamodb import aws_dynamo_controller
from app.dynamodb import dynamodb_resource

application = Flask(__name__)


@application.route('/activities/query_by_activity', methods=['GET'])
def query_by_activity(activity):
    request_data = request.get_json()
    query = aws_dynamo_controller.query_by_activity(activity, dynamodb_resource.set_up_resource())
    return jsonify(query=query)


@application.route('/activities/query_by_date', methods=['GET'])
def query_by_date():
    request_data = request.get_json()
    query = aws_dynamo_controller.query_by_date(request_data, dynamodb_resource.set_up_resource())
    return jsonify(query=query)


if __name__ == '__main__':
    application.run(port='6000')
