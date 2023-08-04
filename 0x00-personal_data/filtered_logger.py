#!/usr/bin/env python3
"""
    Assign RedactingFormatter Class
    Create filter_datum() function
    Create get_logger() function
"""
from typing import List
import re
import logging


PII_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
        Returns the log message obfuscated.
    """
    msg_temp = message

    for field in fields:
        msg_temp = re.sub(field + '=.*?' + separator,
                          field + '=' + redaction + separator, msg_temp)

    return msg_temp


def get_logger() -> logging.Logger:
    """
        Logger should be named 'user_data' and only log up
        to loggin.INFO level. it should not propagate messages
        to other loggers, returns loggin.Logger object.
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """
        Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            Filter values in incoming log records using filter_datum.
        """
        message = filter_datum(self.fields, self.REDACTION,
                               super(RedactingFormatter, self).format(record),
                               self.SEPARATOR)
        return message
