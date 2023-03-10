#!/usr/bin/python3
"""Authentication support"""
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from crud_fastapi.schemas.user import TokenData
from crud_fastapi.schemas.database import get_db
from crud_fastapi.models.base_models import UserModel
from crud_fastapi.settings import settings

OAUTH2 = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.OAUTH2_SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_WEEKS = settings.ACCESS_TOKEN_EXPIRE_WEEKS


def create_token(data: dict):
    """Create a new access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(weeks=ACCESS_TOKEN_EXPIRE_WEEKS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """Verify access token provided by user"""
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = decoded_jwt.get("id")
        print(user_id)
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)

    except JWTError as exc:
        raise credentials_exception from exc

    return token_data


def get_current_user(
        token: str = Depends(OAUTH2),
        db: Session = Depends(get_db)
):
    """Get current user helper"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    user = verify_token(token, credentials_exception)
    query = db.query(UserModel).filter(
        UserModel.id == user.id
    ).first()

    return query
