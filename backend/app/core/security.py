from typing import Union, Any
from jose import jwt
import secrets
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta

ALGORITHM = "HS256"


def verify_password(password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed_password)


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def create_access_token(
        subject: Union[str, Any], type: str, expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=11520
        )
    to_encode = {"exp": expire, "sub": str(subject), "type": type}
    encoded_jwt = jwt.encode(to_encode, secrets.token_urlsafe(32), algorithm=ALGORITHM)
    return encoded_jwt
