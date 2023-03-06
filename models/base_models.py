#!/usr/bin/python3
"""Base model"""
from sqlalchemy import (Column,
                        String, Integer,
                        Text, Boolean,
                        TIMESTAMP, text,
                        ForeignKey, Date
                        )
from sqlalchemy.orm import relationship
from crud_fastapi.schemas.database import Base


class PostModel(Base):
    """PostModel class"""
    __tablename__ = 'posts'
    id = Column(
        Integer, primary_key=True,
        nullable=False
    )
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )
    owner_id = Column(
        Integer,
        ForeignKey(
            column="users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    owner = relationship("UserModel")


class UserModel(Base):
    """User model"""
    __tablename__ = 'users'
    id = Column(
        Integer, primary_key=True,
        nullable=False
    )
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    ph_number = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("FALSE"))
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )


class VoteModel(Base):
    """Votes models"""
    __tablename__ = 'votes'
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True
    )
