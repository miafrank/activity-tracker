from flask import Flask, jsonify, request
from app import aws_dynamo_controller

app = Flask(__name__)


@app.route("/")
def main():
    return "This is the main page"


@app.route("/test")
def get_all_items():
    return jsonify(aws_dynamo_controller.get_items())


@app.route("/json", methods=['POST'])
def init_dummy_request():
    request_data = request.get_json()
    date = request_data['date']
    duration = request_data['duration']
    activity_name = request_data['activity_name']
    return '''
        The date is: {}
        The duration is: {}
        The activity is: {}
    
    '''.format(date, duration, activity_name)


if __name__ == '__main__':
    app.run(port='8080')
