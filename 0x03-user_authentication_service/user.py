#!/usr/bin/env python3
"""
    Create User Model
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column


Base = declarative_base()


class User(Base):
    """
        Assign User Class
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String)
    reset_token = Column(String)
