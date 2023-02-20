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
                dbname="your_dbname",
                user="user",
                password="password",
                cursor_factory=RealDictCursor
        ) as conn:
            cursor = conn.cursor()
            print("Connection established!")
            break
    except Exception as e:
        print(f"Error occurred while connecting to database. {e}")
        time.sleep(2000)


class PostModel(BaseModel):
    """PostModel schema"""
    id: str = uuid.uuid4()
    title: str
    content: str
    created_at: str = datetime.datetime.now()
    updated_at: str = datetime.datetime.now()
    published: bool = False
    rating: Optional[int] = None

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
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"posts": posts}

@app.get("/posts/{id}")
def get_post(id: int):
    """Return post details"""
    post = get_post_by_id(id)
    return {"post": post}

@app.put("/posts/update/{id}")
def update_post(id: int, new_data: PostModel):
    """Updates post details"""
    indx = find_post_index(id)
    new_data_dct = new_data.dict()
    new_data_dct["id"] = id
    my_posts[indx] = new_data_dct
    post = get_post_by_id(id)
    return {"post": post}

@app.delete("/posts/delete/{id}")
def delete_post(id: int, response: Response) -> Response:
    """Delete post"""
    indx = find_post_index(id)
    my_posts.pop(indx)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response.status_code

@app.post("/create/posts")
async def create_post(post: PostModel, response: Response):
    """Create new post"""
    if post:
        response.status_code = status.HTTP_201_CREATED
        my_posts.append(post.dict())
        return {"post": post}
    raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Post not created")