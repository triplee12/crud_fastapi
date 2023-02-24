#!/usr/bin/python3
"""User model"""
from sqlalchemy import (
    Column, String, Integer,
    Boolean, TIMESTAMP,
    Date, text
)
from crud_fastapi.schemas.database import Base


class UserModel(Base):
    """User model"""
    __tablename__ = 'users'
    id = Column(
        Integer, primary_key=True,
        nullable=False, autoincrement="auto",
        index=True
    )
    username = Column(String(length=225), unique=True, nullable=False)
    first_name = Column(String(length=225), nullable=False)
    last_name = Column(String(length=225), nullable=False)
    email = Column(String(length=225), nullable=False, unique=True)
    password = Column(String(length=225), nullable=False)
    dob = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("FALSE"))
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )
