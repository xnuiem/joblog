from flask import Flask, request, jsonify
from error import InvalidUsage
from config import Config
from data import DataSource
from logger import Logger
from job import Job

app = Flask(__name__)
app.config.from_object(Config)

logger = Logger(Config).logger
data_obj = DataSource(Config, logger)


@app.route('/check/<key>', methods=['GET'])
def check_key(key):
    value = data_obj.get(key)
    return value


@app.route('/init/<key>', methods=['GET'])
def init_data(key):
    if key == Config.init_key:
        data_obj.init_data()
        ret = {'message': 'Data Init Complete'}
        return jsonify(ret)
    else:
        raise InvalidUsage('Invalid Key', 400)


@app.route('/job', methods=['POST'])
def create_job():
    Job(data_obj).save()


@app.route('/job/<job_id>', methods=['GET', 'PATCH', 'DELETE'])
def handle_job(job_id):
    if request.method == 'GET':
        return False
    return True


@app.route('/job/<job_id>/interview', methods=['POST'])
def add_interview(job_id):
    return True


@app.route('/job/<job_id>/interview/<int_id>', methods=['GET', 'PATCH', 'DELETE'])
def handle_interview(job_id, int_id):
    return True


@app.route('/jobs', methods=['GET'])
def get_jobs():
    return True


@app.route('/job/<job_id>/interviews', methods=['GET'])
def get_interviews(job_id):
    return True


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error_obj):
    response = jsonify(error_obj.to_dict())
    response.status_code = error_obj.status_code
    return response


if __name__ == '__main__':
    app.run(host="localhost", port="5000")
