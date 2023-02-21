#!/usr/bin/python3
"""Database configuration"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PASSW = "userbame:password"
SQLALCHEMY_DATABASE_URL = f"postgresql://{PASSW}@localhost/yourdb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def get_db():
    """Get the database"""
    db = session_local()
    try:
        yield db
    finally:
        db.close()
