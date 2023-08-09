#!/usr/bin/env python3
"""
    Assign BasicAuth Class.
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
        Assign BasicAuth that Inherits from Auth.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
            Returns the Base64 part of the Authorization header
            of a Basic Authentication.
        """
        if authorization_header is None:
            return None
        elif type(authorization_header) is not str:
            return None
        elif authorization_header.split(' ')[0] != "Basic":
            return None
        else:
            return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
            Returns the decoded value of a Base 64 string
            base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        elif type(base64_authorization_header) is not str:
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
            Returns the user email and passwor dfrom the
            Base64 deocded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        elif type(decoded_base64_authorization_header) is not str:
            return (None, None)
        elif ':' not in decoded_base64_authorization_header:
            return (None, None)

        user_credentials = decoded_base64_authorization_header.split(':')
        return (user_credentials[0], user_credentials[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
            Return User instance based on his email and password.
        """

        if user_email is None or type(user_email) is not str:
            return None
        elif user_pwd is None or type(user_pwd) is not str:
            return None

        users_list = User.search({"email": user_email})
        if len(users_list) == 0:
            return None

        user = users_list[0]

        if user.is_valid_password(user_pwd) is False:
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        """
        if request is None:
            return None

        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None

        deocded_authorization = self.decode_base64_authorization_header(
            self.extract_base64_authorization_header(authorization_header)
        )

        user_credentials = self.extract_user_credentials(deocded_authorization)

        user_instance = self.user_object_from_credentials(user_credentials[0],
                                                          user_credentials[1])
        if user_instance is None:
            return None

        return user_instance
