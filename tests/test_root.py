#!/usr/bin/python3
"""Test for root routers"""


def test_root(client):
    """Testing for root route"""
    res = client.get('/')
    assert res.json().get("message") == "Welcome to my API world!"
    assert res.status_code == 200
