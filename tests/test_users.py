#!/usr/bin/python3
"""Testing file for user module"""
import pytest
from fastapi.testclient import TestClient
from apps.main import app
from schemas import user
from models.base_models import Base
from .database import get_test_db, engine


Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_root():
    """Testing for root route"""
    res = client.get('/')
    assert res.json().get("message") == "Hello, world!"
    assert res.status_code == 200


def test_create_user():
    """Test for creating a user"""
    res = client.post('/users/create', json={
        "username": "testuser",
        "password": "testpassword",
        "email": "testemail@testuser.com",
        "ph_number": "07067280029",
        "first_name": "Emmanuel",
        "last_name": "Ejie",
        "dob": "1999-12-31",
    })
    new_user = user.UserRes(**res.json())
    print(new_user)

    assert new_user.username == "testuser"
    assert res.status_code == 201
