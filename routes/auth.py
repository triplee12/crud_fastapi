#!/usr/bin/python3
"""User authentication file"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from apps.oauth import create_token
from schemas.database import get_db
from schemas.user import AccessToken
from models.base_models import UserModel
from utils.hash_pass import verify_pwd

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=AccessToken)
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """User authentication method"""
    q_username = db.query(UserModel).filter(
        UserModel.username == credentials.username
    ).first()
    # q_email = db.query(UserModel).filter(
    #     UserModel.email == credentials.email
    # ).first()

    if not q_username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    if not verify_pwd(credentials.password, q_username.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    access_token = create_token(
        data={"id": q_username.id, "username": q_username.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}
