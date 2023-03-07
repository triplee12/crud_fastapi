#!/usr/bin/python3
"""Testing file for user module"""
import pytest
from jose import jwt
from crud_fastapi.settings import settings
from crud_fastapi.schemas import user


def test_create_user(client):
    """Test for creating a user"""
    res = client.post('/users/create', json={
        "username": "testuser",
        "password": "testpassword",
        "email": "testemail@testuser.com",
        "ph_number": "0700000000",
        "first_name": "User",
        "last_name": "Testuser",
        "dob": "1999-12-31",
    })
    new_user = user.UserRes(**res.json())

    assert new_user.username == "testuser"
    assert res.status_code == 201


def test_login(client):
    """Test for login method"""
    res = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })

    assert res.status_code == 200


def test_user_token(client):
    """Test access token for validation"""
    SECRET_KEY = settings.OAUTH2_SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    res = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_data = user.AccessToken(**res.json())
    decoded_jwt = jwt.decode(
        login_data.access_token,
        SECRET_KEY, algorithms=[ALGORITHM]
    )
    user_id: int = decoded_jwt.get("id")
    username: str = decoded_jwt.get("username")

    assert user_id == 1
    assert username == "testuser"
    assert login_data.token_type == "bearer"


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("triplee1", "mYpassword", 401),
        ("passwordCantNotBeBlank", "000password", 401),
        ("triplee", None, 422),
        (None, "testpassword", 422),
        (None, None, 422),
        ("", None, 422),
        ("", "", 422),
        (11111, 22231, 401),
        (12.32, 1312.00, 401)
    ]
)
def test_fail_login(client, username, password, status_code):
    """Test unauthorized"""
    res = client.post('/login', data={
        'username': username,
        'password': password
    })
    assert res.status_code == status_code


def test_get_user(client):
    """Test get user by username"""
    res = client.get('/users/testuser')
    data = user.UserRes(**res.json())
    assert isinstance(data, user.UserRes)
    assert res.status_code == 200
