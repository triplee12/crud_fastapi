#!/usr/bin/python3
"""User routes"""
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from crud_fastapi.schemas.database import get_db
from crud_fastapi.models import users
from crud_fastapi.schemas.user import UserSchema, UserRes
from crud_fastapi.utils import hash_pass

route = APIRouter(prefix="/users", tags=["Users"])


@route.post("/create", response_model=UserRes)
async def create_user(
    c_user: UserSchema, response: Response,
    db: Session = Depends(get_db)
):
    """Create new user"""
    hashed_pwd = hash_pass.hash_pwd(c_user.password)
    c_user.password = hashed_pwd
    user = users.UserModel(**c_user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    if user:
        response.status_code = status.HTTP_201_CREATED
        return user
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="User not created. User with username or email already exists"
    )


@route.get("/{username}", response_model=UserRes)
def get_user(username: str, db: Session = Depends(get_db)):
    """Get a user by username"""
    user = db.query(users.UserModel).filter(
        users.UserModel.username == username
    ).first()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
