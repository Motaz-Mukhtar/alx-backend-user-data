#!/usr/bin/env python3
"""
    Define Auth methods
"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """
        encrypt password string.
    """
    return bcrypt.hashpw(bytes(password, 'utf-8'),
                         bcrypt.gensalt())


def _generate_uuid() -> str:
    """
        Generate random ID. (UUID)
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            Resister User.

            Return:
                User()
        """
        try:
            user_record = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user_instance = self._db.add_user(email, hashed_password)
            return user_instance
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
            check user password validation.

            Return:
                bool
        """
        try:
            user_record = self._db.find_user_by(email=email)

            return bcrypt.checkpw(password.encode('utf-8'),
                                  user_record.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
            Create and return session ID

            Return:
                session_id(str)
        """
        try:
            user_record = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user_record.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
            Takes a single session_id and return the
            corresponding User or None.

            Return:
                User
                None
        """
        if session_id is None:
            return None
        try:
            user_record = self._db.find_user_by(session_id=session_id)
            return user_record
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
            The method updates the corresponding user's
            session ID to None.

            Return:
                None
        """
        if user_id is None:
            return None
        try:
            user_record = self._db.find_user_by(id=user_id)
            self._db.update_user(user_record.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
            Find user corresponding to the email.

            Return:
                reset_token(str)
        """
        try:
            user_record = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user_record.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
            Hash the password and update the
            user's hashed_password field.

            Return:
                None
        """
        if reset_token is None or password is None:
            return None

        try:
            user_record = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(hashed_password=hashed_password,
                             reset_token=None)
        return None
