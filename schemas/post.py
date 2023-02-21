#!/usr/bin/python3
"""Post schema"""
from datetime import datetime
from pydantic import BaseModel, root_validator


class Post(BaseModel):
    """Post schema"""
    title: str
    content: str
    published: bool = False
    updated_at: str = datetime.now()

    def __str__(self) -> str:
        return self.title

    class Config:
        """Config"""
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        """Number validator"""
        values["updated_at"] = datetime.now()
        return values
