from typing import Optional
from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Email(BaseModel):
    email: str
