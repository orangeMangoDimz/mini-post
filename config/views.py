from django.shortcuts import render
import logging

class AppLogger:

    def __init__(self, name=None):
        if name is None:
            import __main__
            name = __main__.__name__
        self.logger = logging.getLogger(name)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def critical(self, message):
        self.logger.critical(message)