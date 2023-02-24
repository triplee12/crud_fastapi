#!/usr/bin/python3
"""Hash password"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(password: str) -> CryptContext:
    """Hash password"""
    return pwd_context.hash(password)
