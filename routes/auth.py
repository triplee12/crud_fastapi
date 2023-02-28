#!/usr/bin/python3
"""User authentication file"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud_fastapi.schemas.database import get_db
from crud_fastapi.schemas.user import UserAuth, UserRes
from crud_fastapi.models.users import UserModel
from crud_fastapi.utils.hash_pass import verify_pwd

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=UserRes)
def login(credentials: UserAuth, db: Session = Depends(get_db)):
    """User authentication method"""
    q_username = db.query(UserModel).filter(
        UserModel.username == credentials.username
    ).first()
    # q_email = db.query(UserModel).filter(
    #     UserModel.email == credentials.email
    # ).first()

    if not q_username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )

    if not verify_pwd(credentials.password, q_username.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    return q_username
