#!/usr/bin/env python3
"""
    Create SessionExpAuth Class.
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
        Assign SessionExpAuth Class for expiration
        date to a Session ID.
    """
    def __init__(self):
        try:
            self.session_duration = os.getenv("SESSION_DURATION")
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
            Overload create_session() to parent class.
        """
        session_id = super().create_session(user_id)

        if session_id is None or user_id is None:
            return None
        session_dictionary = {
                "user_id": user_id,
                "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
            Overload user_id_for_session_id() to parent class.
        """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id:
            return None

        if self.session_duration == 0:
            return self.user_id_by_session_id[session_id].get("user_id")
        elif "created_at" not in self.user_id_by_session_id[session_id]:
            return None

        session_duration = timedelta(seconds=int(self.session_duration))
        created_at = self.user_id_by_session_id[session_id].get('created_at')
        if created_at + session_duration < datetime.now():
            return None

        return self.user_id_by_session_id[session_id].get("user_id")
