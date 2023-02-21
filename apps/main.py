#!/usr/bin/python3
"""CRUD API using fastapi and postgresql"""
from fastapi import Depends, FastAPI, Response, status, HTTPException
from sqlalchemy.orm import Session
from crud_fastapi.schemas.database import engine, get_db
from crud_fastapi.schemas.post import Post
from crud_fastapi.models import posts

posts.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    """Root route"""
    return {"messaga": "Welcome to my API world!"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    """Retrives all posts"""
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    all_posts = db.query(posts.PostModel).all()
    return {"posts": all_posts}


@app.get("/posts/{_id}")
def get_post(_id: int, db: Session = Depends(get_db)):
    """Return post details"""
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    post = db.query(posts.PostModel).filter(
        posts.PostModel.id == _id
    ).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found error"
        )
    return {"post": post}


@app.put("/posts/update/{_id}")
def update_post(_id: int, post: Post, db: Session = Depends(get_db)):
    """Updates post details"""
    # cursor.execute(
    #     """
    #     UPDATE posts SET title = %s, content = %s, published = %s,
    #     updated_at = NOW() WHERE id = %s RETURNING *
    #     """, (post.title, post.content, post.published, str(_id),)
    # )
    # updated = cursor.fetchone()
    query = db.query(posts.PostModel).filter(posts.PostModel.id == _id)
    if query.first():
        query.update(post.dict(), synchronize_session=False)
        db.commit()
        return {"post": query.first()}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found error"
    )


@app.delete("/posts/delete/{_id}")
def delete_post(
    _id: int, response: Response,
    db: Session = Depends(get_db)
) -> Response:
    """Delete post"""
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""",
    #     (str(_id),)
    # )
    # deleted = cursor.fetchone()

    to_delete = db.query(posts.PostModel).filter(posts.PostModel.id == _id)

    if to_delete.first():
        to_delete.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return response.status_code
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found error"
    )


@app.post("/create/posts")
async def create_post(
    post: Post,
    response: Response,
    db: Session = Depends(get_db)
):
    """Create new post"""
    # cursor.execute(
    #     """
    #     INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    #     RETURNING *
    #     """,
    #     (post.title, post.content, post.published)
    # )
    # post = cursor.fetchone()
    # conn.commit()
    post = posts.PostModel(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    if post:
        response.status_code = status.HTTP_201_CREATED
        return {"post": post}
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Post not created"
    )
