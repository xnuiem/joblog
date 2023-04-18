import os


class Config(object):
    logging_level = os.getenv('JOBLOG_LOGGING_LEVEL', 'DEBUG')
    logging_file = os.getenv('JOBLOG_LOGGING_FILE', '')
    cache_host = os.getenv('JOBLOG_DATA_HOST', 'localhost')
    cache_port = os.getenv('JOBLOG_DATA_PORT', 6307)
    cache_user = os.getenv('JOBLOG_DATA_USER', 'admin')
    cache_pass = os.getenv('JOBLOG_DATA_PASS', 'admin')
    cache_db = os.getenv('JOBLOG_DATA_DB', 0)
    init_key = os.getenv('JOBLOG_INIT_KEY', '489ahjedlkyhfkilsh')

