#!/usr/bin/python3
"""Test for the votes module"""
import pytest
from crud_fastapi.models.base_models import VoteModel


@pytest.fixture
def voted_post(test_user, session, test_create_post):
    """Pre-vote on post with id 4"""
    res = VoteModel(
        post_id=test_create_post[3].id,
        user_id=test_user["id"]
    )
    session.add(res)
    session.commit()


def test_vote_on_post(authorized_client, test_create_post):
    """Test for voting on post"""
    res = authorized_client.post("/likes", json={
        "post_id": test_create_post[3].id,
        "dir_": 1}
    )

    assert res.status_code == 201


def test_unauthorized_user_vote_on_post(client, test_create_post):
    """Test for unauthorized user voting on post"""
    res = client.post("/likes", json={
        "post_id": test_create_post[0].id,
        "dir_": 1}
    )

    assert res.status_code == 401


def test_vote_on_nonexist_post(authorized_client, test_create_post):
    """Test for voting on non existing post"""
    res = authorized_client.post("/likes", json={"post_id": 6, "dir_": 1})

    assert res.status_code == 404


def test_vote_on_already_voted_post(
        authorized_client,
        test_create_post,
        voted_post
    ):
    """Test for voting on already voted post"""
    res = authorized_client.post("/likes", json={
        "post_id": test_create_post[3].id,
        "dir_": 1}
    )

    assert res.json()["detail"] == "Post already liked"
    assert res.status_code == 409


def test_unvote_on_non_voted_post(
        authorized_client,
        test_create_post
    ):
    """Test for unvoting on non voted post"""
    res = authorized_client.post("/likes", json={
        "post_id": test_create_post[1].id,
        "dir_": 0}
    )

    assert res.json()["detail"] == "Like doesn't exist"
    assert res.status_code == 304


def test_unauthorized_user_unvote_on_post(client, test_create_post):
    """Test for unauthorized user unvoting on post"""
    res = client.post("/likes", json={
        "post_id": test_create_post[0].id,
        "dir_": 0}
    )

    assert res.status_code == 401


def test_user_vote_on_own_post(authorized_client, test_create_post):
    """Test for voting on own post"""
    res = authorized_client.post("/likes", json={
        "post_id": test_create_post[0].id,
        "dir_": 0
        }
    )

    assert res.status_code == 403