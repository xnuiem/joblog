import os


class Config(object):
    logging_level = os.getenv('JOBLOG_LOGGING_LEVEL', 'DEBUG')
    logging_file = os.getenv('JOBLOG_LOGGING_FILE', '')
    cache_host = os.getenv('JOBLOG_DATA_HOST', 'localhost')
    cache_port = os.getenv('JOBLOG_DATA_PORT', 6379)
    cache_db = os.getenv('JOBLOG_DATA_DB', 0)
    init_key = os.getenv('JOBLOG_INIT_KEY', 'alksj3489qyalijo83iqh')

