from flask import request, jsonify
from apiflask import APIFlask

import backend.joblog.data
from backend.joblog.error import InvalidUsage
from backend.joblog.config import Config
from backend.joblog.data import DataSource, initDataOut, initDataIn
from backend.joblog.logger import Logger
from backend.joblog.job import Job
from backend.joblog.option import Option


app = APIFlask(__name__, spec_path='/spec')
app.config.from_object(Config)
app.config['SPEC_FORMAT'] = 'yaml'
app.config['AUTO_404_RESPONSE'] = False


logger = Logger(Config).logger
data_obj = DataSource(Config, logger)


def create_job_obj(job_id=None):
    obj = Job(data_obj, logger)
    if job_id is not None:
        obj.get(job_id)

    return obj


@app.route('/init/<key>', methods=['GET'])
@app.output(initDataOut, examples=backend.joblog.data.dataOutExamples)
def init_data(key):
    """Initialize the base data in Redis

    Adds Status/Reason/Source values to Redis
    """
    logger.info('In init_data')
    if key == Config.init_key:
        logger.info('Key is Valid')
        data_obj.init_data()
        ret = {'message': 'Data Init Complete'}
        return jsonify(ret)
    else:
        raise InvalidUsage('Invalid Key', 400)


@app.route('/clear/<key>', methods=['GET'])
def clear_data(key):
    """CLears the entire datastore

    Should be used to clear all of Redis
    """
    logger.info('In clear')
    if key == Config.init_key:
        data_obj.flush_all()
        ret = {'message': 'Data Flushed'}
        return jsonify(ret)
    else:
        raise InvalidUsage('Invalid Key', 400)


@app.route('/job', methods=['POST'])
def create_job():
    obj = create_job_obj()
    return obj.save()


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
    return job_obj.add_update_interview()


@app.route('/job/<job_id>/interview/<int_id>', methods=['GET', 'PATCH', 'DELETE'])
def handle_interview(job_id, int_id):
    job_obj = create_job_obj(job_id)

    if request.method == 'GET':
        return job_obj.get_interview(int_id)

    elif request.method == 'PATCH':
        return job_obj.add_update_interview(int_id)

    elif request.method == 'DELETE':
        return job_obj.delete_interview(int_id)


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


@app.route('/option/<scope>', methods=['GET', 'PUT'])
def handle_option(scope):
    if request.method == 'GET':
        option_list = Option(data_obj, scope).get_options()
        return jsonify(option_list)

    elif request.method == 'PUT':
        return jsonify(Option(data_obj, scope).update())


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error_obj):
    response = jsonify(error_obj.to_dict())
    response.status_code = error_obj.status_code
    return response


if __name__ == '__main__':
    app.run(host="localhost", port=5000)
