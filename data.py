import redis


class DataSource:
    def __init__(self, config, logger):
        self.logger = logger
        self.count = 0
        self.last_id = 0
        self.source = redis.Redis(host=config.cache_host, port=config.cache_port, db=config.cache_db,
                                  username=config.cache_user, password=config.cache_pass)

    def insert(self, key, value):
        self.source.json().set(key, '$', value)
        return True

    def exists(self, key):
        return self.source.exists(key)

    def flush_all(self):
        self.source.flushall()

    def update(self, key, value):
        self.source.json().set(key, '$', value)
        return True

    def delete(self, key):
        self.source.delete(key)

    def get(self, key):
        return self.source.json().get(key)

    def search(self, term):
        return self.source.keys('*' + term + '*')

    def init_data(self):
        status_list = ['Applied', 'Interviewing', 'On Hold', 'Stale', 'Declined', 'Rejected']
        reason_list = ['Ghost', 'Location', 'Pay', 'Travel', 'Job', 'Other']
        source_list = ['LinkedIn', 'Indeed', 'Direct', 'Recruiter', 'Dice', 'Friend']
        self.insert('status', status_list)
        self.insert('reason', reason_list)
        self.insert('source', source_list)
