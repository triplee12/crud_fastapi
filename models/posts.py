#!/usr/bin/python3
"""Posts model"""
from sqlalchemy import (Column,
                        String, Integer,
                        Text, Boolean,
                        TIMESTAMP, text
                        )
from crud_fastapi.schemas.database import Base


class PostModel(Base):
    """PostModel class"""
    __tablename__ = 'posts'
    id = Column(
        Integer, primary_key=True,
        unique=True, nullable=False,
        autoincrement="auto"
    )
    title = Column(String(length=225), nullable=False)
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
