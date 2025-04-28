from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core import config
from db.db import DBConnector
from src.models.user import User

db_connector = DBConnector()

get_session = db_connector.get_session
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = (datetime.now(timezone.utc) + expires_delta)
    else:
        expire = (datetime.now(timezone.utc) + timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             config.app_settings.secret_key,
                             algorithm=config.app_settings.algorithm)
    return encoded_jwt


async def get_current_user(token, db_session: AsyncSession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                             config.app_settings.secret_key,
                             algorithms=[config.app_settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    statement = select(User).where(User.user_name == username)
    result = await db_session.execute(statement=statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user