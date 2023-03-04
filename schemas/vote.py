#!/usr/bin/python3
"""Like schema"""
from pydantic import BaseModel
from pydantic.types import conint


class LikeSchema(BaseModel):
    """Like schema"""
    post_id: int
    has_liked: bool = False
    dir_: conint(le=1)
