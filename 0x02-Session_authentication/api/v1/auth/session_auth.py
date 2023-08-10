#!/usr/bin/env python3
"""
    Assign SessionAuth Class.
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
        Assign SeesionAuth Class that inherits
        from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
            Create new session id and return the id session.
        """
        if user_id is None or type(user_id) is not str:
            return None

        session_id = uuid.uuid4()

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
            Return a User ID based on a Session ID
        """
        if session_id is None and type(session_id) != str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
            Return a User instance based on a cookie value.
        """
        session_id = self.session_cookie(request)

        user_instance = User.get(self.user_id_for_session_id(session_id))

        return user_instance