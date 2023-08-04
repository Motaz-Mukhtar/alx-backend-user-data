#!/usr/bin/env python3
"""
    Implement hash_password() function and is_valid() function
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
        Returns a salted, hashed password, which
        is a byte string.
    """
    return bcrypt.hashpw(bytes(password, 'utf-8'),
                         bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
        Validate that the provided password matches
        the hashed password.
    """
    if bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password):
        return True
    return False
