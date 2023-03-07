#!/usr/bin/python3
"""Database configuration"""
import pytest
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from crud_fastapi.apps.main import app
from crud_fastapi.models.base_models import Base
from crud_fastapi.schemas.database import get_db
from crud_fastapi.settings import settings

PASSW = settings.DB_USER_PASSW
DB_NAME = settings.DB_NAME
SQLALCHEMY_DATABASE_URL = f"postgresql://{PASSW}@localhost/test_{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
testing_session_local = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)
# Base = declarative_base()


@pytest.fixture(scope="module")
def session():
    """Database session"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    """Return TestClient"""
    def get_test_db():
        """Get the database"""
        try:
            yield session
        finally:
            session.close()
    yield TestClient(app)

    app.dependency_overrides[get_db] = get_test_db