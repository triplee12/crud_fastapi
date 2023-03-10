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
    updated_at: datetime
    created_at: datetime
    owner: UserRes

    class Config:
        """Postresponse configuration"""
        orm_mode = True


class PostVote(BaseModel):
    """Post likes"""
    # post: PostRes
    likes: int

    class Config:
        """Post like response configuration"""
        orm_mode = True
