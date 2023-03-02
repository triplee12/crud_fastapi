#!/usr/bin/python3
"""Likes models"""
from sqlalchemy import ForeignKey, Integer, Column, String
from crud_fastapi.schemas.database import Base


class LikesModel(Base):
    """Likes models"""
    __tablename__ = 'likes'
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE", link_to_name=True),
        nullable=False,
        primary_key=True
    )
    user_username = Column(
        String,
        ForeignKey("users.username", ondelete="CASCADE", link_to_name=True),
        nullable=False,
        primary_key=True
    )
