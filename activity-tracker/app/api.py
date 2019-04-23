from flask import Flask, jsonify, request
from app import aws_dynamo_controller

app = Flask(__name__)


@app.route("/test")
def get_all_items():
    return jsonify(aws_dynamo_controller.get_items())


@app.route("/create-activity", methods=['POST'])
def create_activity():
    request_data = request.get_json()
    save = aws_dynamo_controller.create_item(request_data)
    return jsonify(save)


if __name__ == '__main__':
    app.run(port='8080')
