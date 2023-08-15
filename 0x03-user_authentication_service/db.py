#!/usr/bin/env pyhton3
"""
    Create DB Model
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(email:str, hashed_password: str) -> User:
        """
            Save the user to the database
        """
        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        self._session.add(new_user)
        return new_user

    def find_user_by(**kwargs):
        """
            This method takes in arbitrary keyword arguments
            and returns the first row found in the users table
            as filtered by the method’s input arguments
        """
        for key, value in kwargs.items():
            try:
                user = self._session.query(User).all().\
                        filter_by(key=value)
            except Exception:
                raise InvalidRequestError
        if user == []:
            raise NoResultFound
        return user[0]

    def update_user(user_id: int, **kwargs) -> None:
        """
            The method will use find_user_by to locate the user
            to update, then will update the user’s attributes as
            passed in the method’s arguments then commit changes
            to the database.
        """
        pass
