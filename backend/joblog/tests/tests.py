import pytest
import json
import sys, os, inspect
from backend.joblog import app

cmd_folder = os.path.abspath(os.path.join(os.path.split(inspect.getfile(
    inspect.currentframe()))[0], "../.."))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


@pytest.mark.unittest
class Test_Joblog:

    def __int__(self):
        self.job_id = None

    @classmethod
    def setup_class(cls):
        app.test_client().get('/init/alksj3489qyalijo83iqh')

    @classmethod
    def teardown_class(cls):
        app.test_client().get('/clear/alksj3489qyalijo83iqh')

    @pytest.mark.init
    def test_init_db(self):
        app.test_client().get('/clear/alksj3489qyalijo83iqh')

        response = app.test_client().get('/init/alksj3489qyalijo83iqh')
        res = json.loads(response.data.decode('utf-8')).get("message")

        assert res == 'Data Init Complete'
        assert response.status_code == 200

    @pytest.mark.init
    def test_init_invalid_key(self):
        response = app.test_client().get('/init/lkasdjfklasjdf')
        res = json.loads(response.data.decode('utf-8')).get("message")

        assert res == 'Invalid Key'
        assert response.status_code == 400

    @pytest.mark.option_test
    def test_get_option(self):
        response = app.test_client().get('/option/reason')
        res = json.loads(response.data.decode('utf-8'))

        assert res[2] == 'Pay'

    @pytest.mark.option_test
    def test_update_option(self):
        response = app.test_client().get('/option/reason')
        res = json.loads(response.data.decode('utf-8'))
        res[3] = 'Fail'

        self.send_put('/option/reason', {'data': res})
        response = app.test_client().get('/option/reason')
        res = json.loads(response.data.decode('utf-8'))

        assert res[3] == 'Fail'

    @pytest.mark.job
    def test_add_job(self):
        data = {
            "title": "VP of First",
            "company": "ACME",
            "source": "Direct"
        }

        response = self.send_post('/job', data)
        add_res = json.loads(response.data.decode('utf-8'))
        self.job_id = add_res['id']

        response = app.test_client().get('/job/' + self.job_id)
        res = json.loads(response.data.decode('utf-8'))

        assert res['title'] == add_res['title']
        assert res['title'] == data['title']

    @pytest.mark.job
    def test_edit_job(self):
        data = {
            "title": "VP of First",
            "company": "ACME",
            "source": "Direct"
        }

        response = self.send_post('/job', data)
        add_res = json.loads(response.data.decode('utf-8'))
        self.job_id = add_res['id']

        data = {
            "title": "VP of Second",
            "company": "ACME2",
            "source": "Direct"
        }
        response = self.send_patch('/job/' + self.job_id, data)
        res = json.loads(response.data.decode('utf-8'))

        assert res['title'] == data['title']
        assert res['company'] == data['company']

        response = app.test_client().get('/job/' + self.job_id)
        res = json.loads(response.data.decode('utf-8'))

        assert res['title'] == data['title']
        assert res['company'] == data['company']

    @staticmethod
    def create_headers():
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        return headers

    def send_post(self, url, data):
        return app.test_client().post(url, json=data, headers=self.create_headers())

    def send_put(self, url, data):
        return app.test_client().put(url, json=data, headers=self.create_headers())

    def send_patch(self, url, data):
        return app.test_client().patch(url, json=data, headers=self.create_headers())
