#!/usr/bin/python3
"""Post schema"""
from datetime import datetime
from pydantic import BaseModel, root_validator
from .user import UserRes


class Post(BaseModel):
    """Post schema"""
    title: str
    content: str
    published: bool = False

    def __str__(self) -> str:
        return self.title


class UpdatePost(Post):
    """Update post schema"""
    updated_at: str = datetime.now

    class Config:
        """Config"""
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        """Number validator"""
        values["updated_at"] = datetime.now()
        return values


class PostRes(Post):
    """Post response"""
    id: int
    user_username: str
    updated_at: datetime
    created_at: datetime
    owner: UserRes

    class Config:
        """Postresponse configuration"""
        orm_mode = True
