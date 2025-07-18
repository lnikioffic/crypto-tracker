import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevels(StrEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"


def configure_logging():
    logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO, format=LOG_FORMAT_DEBUG, filename='app.log', filemode="w"
    )
