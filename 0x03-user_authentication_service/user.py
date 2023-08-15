#!/usr/bin/env python3
"""
    Create User Model
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String


base = declarative_base()


class User:
    """
        Assign User Class
    """
    __tablename__ = "users"

    pass
