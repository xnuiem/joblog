


class Option:

    def __init__(self, data, scope):
        self.scope = scope
        self.data = data

    def get_options(self):
        if self.scope is None:
            return False

        return self.data.get(self.scope)

