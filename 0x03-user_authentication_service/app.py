#!/usr/bin/env python3
"""
    Setting up Flask App
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def main():
    """
        Return Message
    """
    return jsonify({"message": "Bienvenue"})
print(dir(request))
@app.route('/users', methods=["POST"], strict_slashes=False)
def users():
    """
        Register new user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    print(type(password))
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000", debug=True)
