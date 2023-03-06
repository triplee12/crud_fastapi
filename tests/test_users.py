#!/usr/bin/python3
"""Testing file for user module"""
import pytest
from fastapi.testclient import TestClient
from crud_fastapi.apps.main import app
from crud_fastapi.schemas import user
from crud_fastapi.models.base_models import Base
from .database import get_test_db, engine


Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_root():
    """Testing for root route"""
    res = client.get('/')
    assert res.json().get("message") == "Welcome to my API world!"
    assert res.status_code == 200


def test_create_user():
    """Test for creating a user"""
    res = client.post('/users/create', json={
        "username": "testuser2",
        "password": "testpassword2",
        "email": "testemail2@testuser.com",
        "ph_number": "0700000002",
        "first_name": "User",
        "last_name": "Testuser",
        "dob": "1999-12-31",
    })
    new_user = user.UserRes(**res.json())
    print(new_user)

    assert new_user.username == "testuser2"
    assert res.status_code == 201
