from flask import request
from datetime import date
from pprint import pprint
from error import InvalidUsage
from option import Option
import uuid


# need a log

class Job:

    def __init__(self, data):
        self.data = data
        self.id = None
        self.title = None
        self.status = None
        self.reason = None
        self.source = None
        self.company = None
        self.recruiter = None
        self.last_active_date = None
        self.create_date = None
        self.offer_date = None
        self.notes = None
        self.interviews = {}

    def validate(self):
        if self.company is None and self.recruiter is None:
            raise InvalidUsage('Company or Recruiter is required', 400)

        if self.title is None:
            raise InvalidUsage('Title is Required', 400)

        if self.reason is not None:
            reasons = Option(self.data, 'reason').get_options()
            if self.reason not in reasons:
                raise InvalidUsage('Invalid Reason', 400)

        if self.source is not None:
            sources = Option(self.data, 'source').get_options()
            if self.source not in sources:
                raise InvalidUsage('Invalid Source', 400)

        if self.status is not None:
            statuses = Option(self.data, 'status').get_options()
            if self.status not in statuses:
                raise InvalidUsage('Invalid Status', 400)

        return True

    def jobDict(self):
        ret = {'company': self.company,
               'id': self.id,
               'interviews': self.interviews,
               'last_active_date': self.last_active_date,
               'create_date': self.create_date,
               'notes': self.notes,
               'offer_date': self.offer_date,
               'reason': self.reason,
               'recruiter': self.recruiter,
               'source': self.source,
               'status': self.status,
               'title': self.title}

        return ret

    def save(self):
        obj = request.get_json()
        if self.id is None:

            for key, value in obj.items():
                setattr(self, key, value)

            setattr(self, 'id', str(uuid.uuid4()))
            setattr(self, 'last_active_date', str(date.today()))
            setattr(self, 'create_date', str(date.today()))
            setattr(self, 'status', 'Applied')

            if self.validate():
                self.data.insert(self.id, self.jobDict())
                return self.jobDict()

            return False

        else:
            setattr(self, 'last_active_date', str(date.today()))
            if self.validate():
                self.data.update(self.id, self.jobDict())
                return self.jobDict()

    def get(self, key=None):
        if key is None:
            raise InvalidUsage('Record Not Found', 404)

        if self.data.exists(key):

            obj = self.data.get(key)

            self.id = obj['id']
            self.title = obj['title']
            self.status = obj['status']
            self.reason = obj['reason']
            self.source = obj['source']
            self.company = obj['company']
            self.recruiter = obj['recruiter']
            self.last_active_date = obj['last_active_date']
            self.create_date = obj['create_date']
            self.offer_date = obj['offer_date']
            self.notes = obj['notes']
            self.interviews = obj['interviews']
            return True

        raise InvalidUsage('Record Not Found', 404)

    def update_from_request(self):
        obj = request.get_json()

        for key, value in obj.items():
            setattr(self, key, value)

        setattr(self, 'last_active_date', str(date.today()))
        if self.validate():
            self.data.update(self.id, self.jobDict())
            return self.jobDict()

    def delete(self):
        self.data.delete(self.id)
        return {'message': self.id + ' deleted'}

    def add_interview(self):
        obj = request.get_json()
        self.interviews.update({ str(uuid.uuid4()): obj['date']})
        self.save()
        return self.jobDict()

    def get_interview(self, int_id):
        if int_id in self.interviews:
            return {int_id: self.interviews[int_id]}

        raise InvalidUsage('Interview Key Not Found', 404)

    def get_list(self):
        return self.data.search('-')



