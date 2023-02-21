#!/usr/bin/python3
"""CRUD API using fastapi and postgresql"""
import datetime
import psycopg2
import uuid
import time
from fastapi import FastAPI, Response, status, HTTPException
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
while True:
    try:
        with psycopg2.connect(
                host="127.0.0.1",
                dbname="dbname",
                user="user",
                password="password",
                cursor_factory=RealDictCursor
        ) as conn:
            cursor = conn.cursor()
            print("Connection established!")
            break
    except Exception as e:
        print(f"Error occurred while connecting to database. \n{e}")
        time.sleep(2000)


class PostModel(BaseModel):
    """PostModel schema"""
    title: str
    content: str
    published: bool = False

    def __str__(self) -> str:
        return self.title


my_posts = [
    {
        "id": 1,  #uuid.uuid4()
        "title": "My Blog",
        "content": "My blog content",
        "rating": 2,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "published": True
    },
    {
        "id": 2, #uuid.uuid4()
        "title": "My Blog 1",
        "content": "My blog content 1",
        "rating": 5,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "published": True
    }
]

def find_post_index(id):
    """Return post index else 404 NOT FOUND"""
    for indx, post in enumerate(my_posts):
        if post["id"] == id:
            return indx
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post Not Found")

def get_post_by_id(id):
    """Return post details else 404 NOT FOUND"""
    for post in my_posts:
        if post["id"] == id:
            return post
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post Not Found")

@app.get("/")
async def root():
    return {"messaga": "Welcome to my API world!"}

@app.get("/posts")
async def get_posts():
    """Retrives all posts"""
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"posts": posts}

@app.get("/posts/{id}")
def get_post(id: int):
    """Return post details"""
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found error")
    return {"post": post}

@app.put("/posts/update/{id}")
def update_post(id: int, post: PostModel):
    """Updates post details"""
    cursor.execute(
        """
        UPDATE posts SET title = %s, content = %s, published = %s,
        updated_at = NOW() WHERE id = %s RETURNING *
        """, (post.title, post.content, post.published, str(id),)
    )
    updated = cursor.fetchone()
    if updated:
        conn.commit()
        return {"post": updated}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found error")

@app.delete("/posts/delete/{id}")
def delete_post(id: int, response: Response) -> Response:
    """Delete post"""
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted = cursor.fetchone()
    if deleted:
        conn.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return response.status_code
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found error")

@app.post("/create/posts")
async def create_post(post: PostModel, response: Response):
    """Create new post"""
    cursor.execute(
        """
        INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) 
        RETURNING *
        """,
        (post.title, post.content, post.published)
    )
    post = cursor.fetchone()
    conn.commit()
    if post:
        response.status_code = status.HTTP_201_CREATED
        return {"post": post}
    raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Post not created")