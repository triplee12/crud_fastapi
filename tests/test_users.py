#!/usr/bin/python3
"""Testing file for user module"""
from crud_fastapi.schemas import user
from .database import session, client


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
    pass
