#!/usr/bin/python3
"""User schema definition"""
from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    """User schema definition"""
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    ph_number: str
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
    ph_number: str
    dob: date

    class Config:
        """Configure UserRes object to dictionary"""
        orm_mode = True


class UserAuth(BaseModel):
    """User Auth schema class"""
    username: str
    email: Optional[EmailStr] = None
    password: str


class AccessToken(BaseModel):
    """Access Token schema class"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema"""
    id: Optional[int] = None
