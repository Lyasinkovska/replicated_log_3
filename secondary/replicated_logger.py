import logging


class LoggingHandler(logging.StreamHandler):

    def __init__(self):
        logging.StreamHandler.__init__(self)
        fmt = '%(asctime)s [%(levelname)s] %(message)s'
        formatter = logging.Formatter(fmt)
        self.setFormatter(formatter)


logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
logger.addHandler(LoggingHandler())
