#!/usr/bin/env python3
"""
    Assign SessionAuth Class.
"""
import uuid
from api.v1.auth.auth import Auth


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
