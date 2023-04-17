import logging


class Logger:

    def __init__(self, config):
        self.config = config

        logging.basicConfig(level=config.logging_level)
        logger = logging.getLogger(__name__)

        if config.logging_file:
            handler = logging.FileHandler(config.logging_file)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        self.logger = logger
        self.logger.info('Starting')
        self.logger.debug('===========================')
        self.logger.debug('Configuration')
        self.logger.debug('LOGGING level:%s, file:%s', self.config.logging_level, self.config.logging_file)
        self.logger.debug('CACHE host:%s, port:%s, db:%s', self.config.cache_host,
                          self.config.cache_port, self.config.cache_db)
        self.logger.debug('===========================')
