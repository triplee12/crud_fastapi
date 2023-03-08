#!/usr/bin/python3
"""Testing module for posts module"""


from crud_fastapi.schemas import post


def test_get_posts(authorized_client, test_create_post):
    """Test for list of posts (a.k.a: all posts)"""
    res = authorized_client.get("/posts")
    assert res.status_code == 200


def test_unauthorized_get_posts(client, test_user, test_create_post):
    """Test for unauthorized access to posts"""
    res = client.get("/posts")

    assert res.status_code == 200


def test_get_one_post(client, test_user, test_create_post):
    """Test for access to a post"""
    res = client.get("/posts/1")
    # post_d = post.PostRes(**res.json())
    # assert isinstance(post_d, post.PostRes)
    assert res.status_code == 200


def test_get_one_post_404_error(client):
    """Test for access to a post"""
    res = client.get("/posts/4")

    assert res.status_code == 404


def test_create_post(authorized_client, test_user, test_create_post):
    """Test for creating a post"""
    res = authorized_client.post("/posts/create", json={
        "title": "Create post from test client",
        "content": "test content from test client",
        "published": True
    })
    assert res.status_code == 201


def test_unauthorized_create_post(client, test_user, test_create_post):
    """Test for creating a post"""
    res = client.post("/posts/create", json={
        "title": "Create post from test client",
        "content": "test content from test client"
    })
    assert res.status_code == 401


def test_post_update(authorized_client, test_user, test_create_post):
    """Test for access to a post"""
    res = authorized_client.put(f"/posts/update/{test_create_post[0].id}", json={
        "title": "Updated Title",
        "content": "Updated content",
        "id": test_create_post[0].id
    })

    assert res.status_code == 201


def test_unauthorized_post_update(client, test_user, test_create_post):
    """Test for unauthorized access to update a post"""
    res = client.put(f"/posts/update/{test_create_post[0].id}", json={
        "title": "Updated Title client error",
        "content": "Updated content client error",
        "id": test_create_post[0].id
    })

    assert res.status_code == 401


def test_post_update_nonexist(
        authorized_client,
        test_user,
        test_create_post
    ):
    """Test for unauthorized access to update a post"""
    res = authorized_client.put("/posts/update/100", json={
        "title": "Updated Title client error",
        "content": "Updated content client error",
        "id": 100
    })

    assert res.status_code == 404


def test_update_other_users_post(
        authorized_client,
        test_user,
        test_create_post,
        test_user1
    ):
    """Test for unauthorized access to update a post"""
    res = authorized_client.put(f"/posts/update/{test_create_post[3].id}", json={
        "title": "Updated Title client error",
        "content": "Updated content client error",
        "id": test_create_post[3].id
    })

    assert res.status_code == 403


def test_post_delete(authorized_client, test_user, test_create_post):
    """Test for post deletion"""
    res = authorized_client.delete(f"/posts/delete/{test_create_post[0].id}")

    assert res.status_code == 204


def test_unauthorized_post_delete(client, test_user, test_create_post):
    """Test for unauthorized access to delete a post"""
    res = client.delete(f"/posts/delete/{test_create_post[0].id}")

    assert res.status_code == 401


def test_post_delete_nonexist(authorized_client, test_user, test_create_post):
    """Test for post deletion"""
    res = authorized_client.delete("/posts/delete/10")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_create_post):
    """Test for post deletion"""
    res = authorized_client.delete(f"/posts/delete/{test_create_post[3].id}")

    assert res.status_code == 403
