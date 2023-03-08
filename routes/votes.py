#!/usr/bin/python3
"""Likes routers"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud_fastapi.schemas.database import get_db
from crud_fastapi.models.base_models import VoteModel, PostModel
from crud_fastapi.apps.oauth import get_current_user
from crud_fastapi.schemas.vote import LikeSchema

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def like_router(
    like: LikeSchema, db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Like post router"""
    post = db.query(PostModel).filter(PostModel.id == like.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    user = current_user
    check_like = db.query(VoteModel).filter(
        VoteModel.post_id == like.post_id,
        VoteModel.user_id == user.id
    )
    liked = check_like.first()

    if user.id == post.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to like this post"
        )
    elif int(like.dir_) == 1:
        if liked:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Post already liked"
            )
        to_like = VoteModel(post_id=like.post_id, user_id=user.id)
        db.add(to_like)
        db.commit()
        like.has_liked = True
        return {"has_liked": True}
    else:
        if not liked:
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail="Like doesn't exist"
            )
        check_like.delete(synchronize_session=False)
        db.commit()
        like.has_liked = False
        return {"has_liked": False}
