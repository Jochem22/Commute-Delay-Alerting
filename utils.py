from logging.handlers import RotatingFileHandler
import logging


class Logger:
    def __init__(self):
        self.filename = "main.log"
        logging.basicConfig(
            format='%(asctime)s | %(levelname)s | %(message)s',
            level=logging.DEBUG,
            handlers=[RotatingFileHandler(self.filename, maxBytes=100000, backupCount=5)]
        )

    @staticmethod
    def debug(debug):
        logging.debug(debug)

    @staticmethod
    def info(info):
        logging.info(info)

    @staticmethod
    def warning(warning):
        logging.warning(warning)

    @staticmethod
    def error(error):
        logging.error(error)
