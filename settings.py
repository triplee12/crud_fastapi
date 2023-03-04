#!/usr/bin/python3
"""Base settings for the application"""
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings for environment variables"""
    OAUTH2_SECRET_KEY: str = os.getenv('OAUTH2_SECRET_KEY')
    DB_USER_PASSW: str = os.getenv("DB_USER_PASSW")
    DB_NAME: str = os.getenv("DB_NAME")


settings = Settings()
