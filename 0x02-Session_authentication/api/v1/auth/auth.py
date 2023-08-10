#!/usr/bin/env python3
"""
    Assign Auth Class.
"""
from flask import request
from models.user import User
from typing import List, TypeVar
import os


class Auth:
    """
        Authintication Class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns True if the path is not in
        the list of strings excluded_paths:

        Returns True if path is None
        Returns True if excluded_paths is None or empty
        Returns False if path is in excluded_paths
        You can assume excluded_paths
        contains string path always ending by a /
        This method must be slash tolerant: path=/api/v1/status
        and path=/api/v1/status/ must be returned False if
        excluded_paths contains /api/v1/status/
        """
        if path is not None and path[-1] != '/':
            path += '/'

        if excluded_paths is None or excluded_paths == []:
            return True
        elif path is None:
            return True
        elif path not in excluded_paths:
            return True
        elif path in excluded_paths:
            return False
        return False

    def authorization_header(self, request=None) -> str:
        """
        If request is None, returns None
        If request doesn’t contain the header key Authorization, returns None
        Otherwise, return the value of the header request Authorization
        """
        if request is None:
            return None
        elif 'Authorization' not in request.headers:
            return None
        else:
            return request.headers['Authorization']
        return None

    def current_user(self, request=None):
        """
            Placeholder
            Return None
        """
        return None

    def session_cookie(self, request=None):
        """
            Returns a cookie value from a request
        """
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME")

        return request.cookies.get(session_name)
