from flask import Flask, jsonify
from app import aws_dynamo_controller

app = Flask(__name__)


@app.route("/")
def main():
    return "This is the main page"


@app.route("/test")
def test():
    return jsonify(aws_dynamo_controller.get_items())


if __name__ == '__main__':
    app.run(port='8080')
