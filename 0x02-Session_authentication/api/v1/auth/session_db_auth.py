#!/usr/bin/env python3
"""
    Create SessionDBAuth Class.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
        Assign SessionDBAuth Class that inherits from
        SessionExpAuth.
    """
    def create_session(self, user_id=None):
        """
            Overload create_session():
            that creates and stores new instance
            of UserSession and return the Session ID
        """
        if user_id is None:
            return None
        session_id = super().create_session(user_id)

        user_session = UserSession(session_id=session_id,
                                   user_id=user_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
            Overload user_id_for_session_id():
            Returns the User ID by requesting UserSession
            in the database based on session_id
        """
        res = super().user_id_for_session_id(session_id)
        if res is None:
            return None

        user_session = UserSession.search({"session_id": session_id})
        if user_session == []:
            return None
        for user in user_session:
            if user.to_json().get('user_id'):
                return user.to_json().get('user_id')

    def destroy_session(self, request=None):
        """
            Overload destroy_session:
            Destorys the UserSession based on the Session ID
            from the request cookie.
        """
        session_id = self.session_cookie(request)
        user_session = UserSession.search({"session_id": session_id})
        if user_session is None:
            return None
        for user in user_session:
            user.remove()
