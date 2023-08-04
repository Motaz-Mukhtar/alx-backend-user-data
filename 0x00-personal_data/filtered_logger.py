#!/usr/bin/env python3
"""
    Assign RedactingFormatter Class
    Create filter_datum() function
    Create get_logger() function
"""
from typing import List
import re
import logging
import os
from mysql.connector import connection


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


def get_db() -> connection.MySQLConnection:
    """
        Establish Connection to the database using
        mysql.connection module.
    """
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.environ.get('PERSONAL_DATA_DB_NAME')

    connect = connection.MySQLConnection(
        username=username,
        password=password,
        host=host,
        database=database)

    return connect


class RedactingFormatter(logging.Formatter):
    """
        Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum."""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def main():
    """
        The function will obtain a database connetion using
        get_db() and retrieve all rows in the users table.
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")
    fetch = cursor.fetchall()

    logger = get_logger()

    for row in fetch:
        fields = "name={};email={};phone={};ssn={};\
                  password={};ip={},last_login={};user_agent={}".format(
                          row[0], row[1], row[2], row[3], row[4], row[5],
                          row[6], row[7])
        logger.info(fields)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
