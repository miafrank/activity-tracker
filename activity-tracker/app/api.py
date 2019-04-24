from flask import Flask, jsonify, request
from app import aws_dynamo_controller

app = Flask(__name__)


@app.route("/activity")
def get_all_items():
    return jsonify(aws_dynamo_controller.get_items())


@app.route("/create-activity", methods=['POST'])
def create_activity():
    request_data = request.get_json()
    save = aws_dynamo_controller.create_item(request_data)
    return jsonify(save)


@app.route("/get_activity_by_id/<activity_id>", methods=['GET'])
def get_activity_by_id(activity_id):
    item = aws_dynamo_controller.get_item_by_id(activity_id)
    print(item)
    return jsonify(item)


if __name__ == '__main__':
    app.run(port='8080')
