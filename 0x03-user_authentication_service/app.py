#!/usr/bin/env python3
"""
    Setting up Flask App
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def main():
    """
        Return Message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def users() -> str:
    """
        Register new user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        new_user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    if new_user is not None:
        return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login() -> str:
    """
        Create a new sessionfor the user, store it the
        session ID as a cookie with key 'session_id' on
        the response and return a JSON payload of the form.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)

    if not valid_login:
        abort(401)

    new_session = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})

    response.set_cookie("session_id", new_session)
    return response


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """
        Find the user with the requested session ID. If the user
        exists destroy the session and redirect the user to GET '/'
        if te user does not exists, respond with a 403 HTTP status
    """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)

    if user is None or session_id is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
        respond to the GET /profile route

        Return:
            {'email': '<user email>'} JSON payload
    """
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def reset_password():
    """
        POST /reset_password route
        Generate token

        Return:
            {'email': '<user email>', 'reset_token': '<reset token>'}
            JSON payload
    """
    email = request.form.get("email")
    registered = AUTH.create_session(email)

    if not registered:
        abort(403)

    reset_token = AUTH.get_reset_password_token(email)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route('/reset_password', methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
        PUT /reset_password route
        Update the user password

        Return:
            {'email': '<user email>', 'message': 'Password updated'}
            JSON payload
            if token is invalid
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)

    message = {"email": email, "message": "Password updated"}
    return jsonify(message), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000")
