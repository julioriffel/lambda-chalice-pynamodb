import datetime
import hashlib
import os
from uuid import uuid4

import jwt

from chalicelib.model.user import UserTable

_SECRET = os.getenv("JWT_SECRET", None)


def encode_password(password: str, salt=None):
    if salt is None:
        salt = os.urandom(16)
    hash_name = "sha256"
    rounds = 100000
    hashed = hashlib.pbkdf2_hmac(hash_name, password.encode(), salt, rounds)
    return {
        "hash": hash_name,
        "salt": salt,
        "rounds": rounds,
        "hashed": hashed,
    }


def verify_password(salt, stored_pw_hash, provided_password: str, rounds=100000):
    """Verify a stored password against one provided by user"""

    pw_hash = hashlib.pbkdf2_hmac("sha256", provided_password.encode(), salt, rounds)
    return pw_hash == stored_pw_hash


def decode_jwt_token(token: str):
    token = token.replace("Bearer ", "")
    return jwt.decode(token, _SECRET, algorithms=["HS256"])


def generate_jwt_token(username: str, name: str = None, is_superuser: bool = False):
    now = datetime.datetime.utcnow()
    unique_id = str(uuid4())
    payload = {
        "sub": username,
        "name": name,
        "is_superuser": is_superuser,
        "iat": now,
        "nbf": now,
        "jti": unique_id,
        "exp": now + datetime.timedelta(hours=24),
    }
    return {"token": jwt.encode(payload, _SECRET, algorithm="HS256")}


def login(record: UserTable, password):
    if verify_password(record.salt, record.hashed, password, record.rounds):
        return generate_jwt_token(record.username, record.name, record.is_superuser)
