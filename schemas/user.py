#!/usr/bin/python3
"""User schema definition"""
from datetime import date
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    """User schema definition"""
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    dob: date

    def __str__(self) -> str:
        return self.username


class UserRes(BaseModel):
    """User response schema"""
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    dob: date

    class Config:
        """Configure UserRes object to dictionary"""
        orm_mode = True
