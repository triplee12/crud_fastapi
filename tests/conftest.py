#!/usr/bin/python3
"""Database configuration"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from crud_fastapi.apps.main import app
from crud_fastapi.apps.oauth import create_token
from crud_fastapi.models.base_models import Base, PostModel, UserModel
from crud_fastapi.schemas.database import get_db
from crud_fastapi.settings import settings
from crud_fastapi.schemas import user

PASSW = settings.DB_USER_PASSW
DB_NAME = settings.DB_NAME
SQLALCHEMY_DATABASE_URL = f"postgresql://{PASSW}@localhost/{DB_NAME}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
testing_session_local = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)


@pytest.fixture
def session():
    """Fixture: Database session"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    """Fixture: Return TestClient"""
    def get_test_db():
        """Get the database"""
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    """Create a generic test user"""

    # user_data = UserModel(
    #     username="testuser1",
    #     password="testpassword1",
    #     email="testemail1@testuser.com",
    #     ph_number="0700000001",
    #     first_name="User",
    #     last_name="Testuser",
    #     dob="1999-12-31"
    # )
    # session.add(user_data)
    # session.commit()
    # query = session.query(
    #     UserModel
    # ).filter(UserModel.username == "testuser1").first()

    # return query

    user_data1 = {
        "username": "testuser1",
        "password": "testpassword1",
        "email": "testemail1@testuser.com",
        "ph_number": "0700000001",
        "first_name": "User",
        "last_name": "Testuser",
        "dob": "1999-12-31"
    }
    res = client.post("/users/create", json=user_data1)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data1["password"]
    return new_user


@pytest.fixture
def test_user1(client):
    """Create a generic test user"""
    user_data1 = {
        "username": "testuser2",
        "password": "testpassword1",
        "email": "testemail2@testuser.com",
        "ph_number": "0700000002",
        "first_name": "User",
        "last_name": "Testuser",
        "dob": "1999-12-31"
    }
    res = client.post("/users/create", json=user_data1)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data1["password"]
    return new_user


@pytest.fixture
def token(test_user):
    """Fixture: Create token for testuser"""
    access_token = create_token(
        data={
            "id": test_user["id"],
            "username": test_user["username"]
        }
    )
    return access_token


@pytest.fixture
def authorized_client(client, token):
    """Fixture: Authorize client fixture"""
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer: {token}"
    }
    return client


def convert_post(data):
    """convert data to post model object"""
    return PostModel(**data)


@pytest.fixture
def test_create_post(test_user, session, test_user1):
    """Test creating post"""
    res = [
        {
            "title": "Testing post creation",
            "content": "Testing post content",
            "published": True,
            "owner_id": test_user["id"]
        },
        {
            "title": "Testing post creation 1",
            "content": "Testing post content 1",
            "published": False,
            "owner_id": test_user["id"]
        },
        {
            "title": "Testing post creation 2",
            "content": "Testing post content 2",
            "published": True,
            "owner_id": test_user["id"]
        },
        {
            "title": "Testing post creation 3",
            "content": "Testing post content 3",
            "published": False,
            "owner_id": test_user1["id"]
        }
    ]
    post_data = list(map(convert_post, res))
    session.add_all(post_data)
    session.commit()
    data = session.query(PostModel).all()
    return data
