#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = os.getenv('AUTH_TYPE')


if auth == "basic_auth":
    auth = BasicAuth()
elif auth == "session_auth":
    auth = SessionAuth()
else:
    auth = Auth()


@app.before_request
def before_request():
    """
    if auth is None, do nothing.
    if request.path is not part of this list
    ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'],
    do nothing - you must use the method require_auth from the auth instance.
    if auth.authorization_header(request) returns None,
    raise the error 401 - you must use abort
    if auth.current_user(request) returns None,
    raise the error 403 - you must use abort
    """
    excluded_list = ['/api/v1/status/',
                     '/api/v1/unauthorized/', '/api/v1/forbidden/',
                     '/api/v1/auth_session/login/']
    if auth is None:
        return None
    elif auth.require_auth(request.path, excluded_list) is False:
        return None
    elif auth.current_user(request) is None:
        abort(403)
    elif auth.require_auth(request.path, exlucded_list):
        if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
            abort(401)
        if auth.currnet_user(request) is None:
            abort(403)

    request.currnet_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
        Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
        Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
