#!/usr/bin/env python3
"""
    Define Auth methods
"""
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
import bcrypt


def _hash_password(password: str) -> bytes:
    """
        encrypt password string.
    """
    return bcrypt.hashpw(bytes(password, 'utf-8'),
                         bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            Resister User.
        """
        try:
            user_record = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user_instance = self._db.add_user(email, hashed_password)
            return user_instance
        raise ValueError

    def valid_login(self, email: str, password: str) -> bool:
        """
            check user password validation.
        """
        user_record = self._db.find_user_by(email=email)

        if bcrypt.checkpw(bytes(password, 'utf-8'), user_record.hashed_password):
            return True
        return False
