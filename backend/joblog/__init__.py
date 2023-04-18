from flask import Flask, request, jsonify
from error import InvalidUsage
from config import Config
from data import DataSource
from logger import Logger
from job import Job
from pprint import pprint

app = Flask(__name__)
app.config.from_object(Config)

logger = Logger(Config).logger
data_obj = DataSource(Config, logger)


def create_job_obj(job_id=None):
    obj = Job(data_obj)
    if job_id is not None:
        obj.get(job_id)

    return obj


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
    return Job(data_obj).save()


@app.route('/job/<job_id>', methods=['GET', 'PATCH', 'DELETE'])
def handle_job(job_id):
    job_obj = create_job_obj(job_id)

    if request.method == 'GET':
        return job_obj.jobDict()

    elif request.method == 'PATCH':
        job_obj.update_from_request()
        return job_obj.save()

    elif request.method == 'DELETE':
        return job_obj.delete()


@app.route('/job/<job_id>/interview', methods=['POST'])
def add_interview(job_id):
    job_obj = create_job_obj(job_id)
    return job_obj.add_interview()


@app.route('/job/<job_id>/interview/<int_id>', methods=['GET', 'PATCH', 'DELETE'])
def handle_interview(job_id, int_id):
    job_obj = create_job_obj(job_id)

    if request.method == 'GET':
        return job_obj.get_interview(int_id)

    elif request.method == 'PATCH':
        job_obj.update_from_request()
        return job_obj.save()

    elif request.method == 'DELETE':
        return job_obj.delete()


@app.route('/jobs', methods=['GET'])
def get_jobs():
    job_list = {}
    job_obj = create_job_obj()
    jobs = job_obj.get_list()
    for i in jobs:
        job_obj.get(i)
        job_list.update({job_obj.id: job_obj.jobDict()})

    return jsonify(job_list)


@app.route('/job/<job_id>/interviews', methods=['GET'])
def get_interviews(job_id):
    job_obj = create_job_obj(job_id)
    return dict(job_obj.interviews)


@app.route('/option/<scope>', methods=['GET', 'PATCH'])
def handle_option(scope):
    if request.method == 'GET':
        return True
    elif request.method == 'PATCH':
        return True


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error_obj):
    response = jsonify(error_obj.to_dict())
    response.status_code = error_obj.status_code
    return response


if __name__ == '__main__':
    app.run(host="localhost", port="5000")
