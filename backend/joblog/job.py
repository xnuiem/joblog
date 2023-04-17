from flask import request
from datetime import date
from pprint import pprint


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
        self.last_activity = None
        self.offer_date = None
        self.notes = None
        self.interviews = []

    def validate(self):
        #requried present
        #lists valid

        return True

    def jobDict(self):
        ret = {'company': self.company,
               'id': self.id,
               'interviews': self.interviews,
               'last_activity': self.last_activity,
               'notes': self.notes,
               'offer_date': self.offer_date,
               'reason': self.reason,
               'recruiter': self.recruiter,
               'source': self.source,
               'status': self.status,
               'title': self.title}

        return ret

    def save(self):
        if self.id is None:
            obj = request.get_json()
            for key, value in obj.items():
                setattr(self, key, value)

            setattr(self, 'last_activity', str(date.today()))
            setattr(self, 'status', 'Applied')

            pprint(self.jobDict())
            if self.validate():
                self.id = self.data.insert(self.jobDict())
                return True

            message = 'Validation Error'
            return False

        else:
            #update
            return True



    def get(self, id=None):
        if id is None:
            print("ADD")
            # this is an add
        else:
            print("GET")
            # this is a get

        return True
