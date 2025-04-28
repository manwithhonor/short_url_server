from datetime import timedelta

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer
from core import config
from db.db import DBConnector
from src.auth import auth_handler
from src.models.user import User as user_model
from src.schemas.user import User as user_schema
from src.schemas.user import UserFromDB
from typing import Annotated

db_connector = DBConnector()
get_session = db_connector.get_session
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/signup",
             status_code=status.HTTP_201_CREATED,
             response_model=int,
             summary = 'Добавить пользователя')
async def create_user(user: user_schema,
                session: AsyncSession = Depends(get_session)):
    new_user = user_model(
        user_name=user.user_name,
        password=auth_handler.get_password_hash(user.password)
    )
    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user.user_id
    except IntegrityError as e:
        # assert isinstance(e.orig, UniqueViolation)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User with user_name {user.user_name} already exists"
        )


@router.post("/login",
             status_code=status.HTTP_200_OK,
             summary = 'Войти в систему')
async def user_login(login_attempt_data: OAuth2PasswordRequestForm = Depends(),
                     db_session: AsyncSession = Depends(get_session)):

    statement = select(user_model).where(user_model.user_name == login_attempt_data.username)
    result = await db_session.execute(statement=statement)
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {login_attempt_data.username} not found"
        )

    if auth_handler.verify_password(login_attempt_data.password, existing_user.password):
        access_token_expires = timedelta(minutes=config.app_settings.access_token_expire_minutes)
        access_token = auth_handler.create_access_token(
            data={"sub": login_attempt_data.username},
            expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Wrong password for user {login_attempt_data.username}"
        )

@router.get("/test-auth")
def show_access_token(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@router.get("/me",
            response_model=int,
            summary = 'Получить ID вошедшего пользователя')
async def get_current_user(token: str = Depends(oauth2_scheme),
                     db_session: AsyncSession = Depends(get_session)):
    current_user = await auth_handler.get_current_user(token, db_session)
    return current_user.user_id
