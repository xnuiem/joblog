from flask import request
from error import InvalidUsage


class Option:

    def __init__(self, data, scope=None):
        self.scope = scope
        self.data = data

    def get_options(self):
        if self.scope is None:
            raise InvalidUsage('Invalid Scope', 404)

        return self.data.get(self.scope)

    def update(self):
        obj = request.get_json()
        self.data.update(self.scope, obj['data'])
        return self.get_options()
