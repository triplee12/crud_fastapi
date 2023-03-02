#!/usr/bin/python3
"""Base settings for the application"""
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings for environment variables"""
    OAUTH2_SECRET_KEY: str
    DB_USER_PASSW: str
    DB_NAME: str

    class Config:
        """Configuration path"""
        env_file = os.getenv("PATH")


settings = Settings()
