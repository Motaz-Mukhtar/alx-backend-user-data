#!/usr/bin/env python3
"""
    Handles all routes for the Session Auth
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def authentication_login():
    """
        Login User authentication.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    if password is None or password == "":
        return jsonify({"error": "password"}), 400

    user = None
    for users in User.search({"email": email}):
        user = users
        break

    if user is None:
        return jsonify({"error": "no user found for this email"}), 404

    if user.is_valid_password(password) is False:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())

    response.set_cookie(os.getenv("SESSION_NAME"), session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def authentication_logout():
    """
        Logout User authentication.
    """
    from api.v1.app import auth

    logout = auth.destroy_session(request)
    if logout is False:
        abort(404)

    return jsonify({}), 200
