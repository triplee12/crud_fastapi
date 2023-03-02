#!/usr/bin/python3
"""Posts routes"""
from typing import List, Optional
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from crud_fastapi.schemas.database import get_db
from crud_fastapi.apps.oauth import get_current_user
from crud_fastapi.models import posts, likes
from crud_fastapi.schemas.post import (
    Post, PostRes, UpdatePost, PostLike
)

route = APIRouter(prefix="/posts", tags=["Posts"])


@route.get("/", response_model=List[PostLike])
async def get_posts(
    db: Session = Depends(get_db),
    limit: int = 100,
    skip: int = 0,
    search: Optional[str] = ''
):
    """Retrives all posts"""
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    all_posts = db.query(posts.PostModel).filter(
        posts.PostModel.content.icontains(search)
    ).filter(
        posts.PostModel.title.icontains(search)
    ).limit(limit).offset(skip).all()

    like_posts = db.query(posts.PostModel,
        func.count(likes.LikesModel.post_id).label("likes")
    ).join(
        likes.LikesModel,
        likes.LikesModel.post_id == posts.PostModel.id,
        isouter=True
    ).group_by(posts.PostModel.id).all()

    return like_posts


@route.get("/{_id}", response_model=PostRes)
def get_post(_id: int, db: Session = Depends(get_db)):
    """Return a post details"""
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
    return post


@route.put("/update/{_id}", response_model=PostRes)
def update_post(
    _id: int, post: UpdatePost,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Updates post details"""
    # cursor.execute(
    #     """
    #     UPDATE posts SET title = %s, content = %s, published = %s,
    #     updated_at = NOW() WHERE id = %s RETURNING *
    #     """, (post.title, post.content, post.published, str(_id),)
    # )
    # updated = cursor.fetchone()
    query = db.query(posts.PostModel).filter(posts.PostModel.id == _id)
    if query.first().user_username == current_user.username:
        query.update(post.dict(), synchronize_session=False)
        db.commit()
        return query.first()
    elif query.first().user_username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied!"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found error"
    )


@route.delete("/delete/{_id}")
def delete_post(
    _id: int, response: Response,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
) -> Response:
    """Delete post"""
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""",
    #     (str(_id),)
    # )
    # deleted = cursor.fetchone()

    to_delete = db.query(posts.PostModel).filter(posts.PostModel.id == _id)

    if to_delete.first().user_username == current_user.username:
        to_delete.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return response.status_code
    elif to_delete.first().user_username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied!"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found error"
    )


@route.post("/create", response_model=PostRes)
async def create_post(
    post: Post,
    response: Response,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
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

    owner = current_user.username
    post = posts.PostModel(user_username=owner, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    if post:
        response.status_code = status.HTTP_201_CREATED
        return post
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Post not created"
    )
