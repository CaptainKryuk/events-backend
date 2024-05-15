import base64
import datetime
import hashlib
from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.db.connection import get_pgsql_session
from app.db.models import User, Session
import jwt

router = APIRouter()


class UserRegistrationData(BaseModel):
    email: EmailStr
    login: str
    password: str
    confirm_password: str


class UserLoginData(BaseModel):
    login: str
    password: str


class ListUserEntity(BaseModel):
    id: int
    username: str


class UserEntity(BaseModel):
    id: int
    username: str
    email: str


@router.post('/registration')
async def register_user(
    data: UserRegistrationData,
    session: AsyncSession = Depends(get_pgsql_session)
):
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail='Пароли не совпадают')

    exist_user = (await session.execute(select(User).where(User.username == data.login))).scalars().one_or_none()
    if exist_user:
        raise HTTPException(status_code=400, detail='Пользователь с таким username уже существует')

    s = hashlib.md5(data.password.encode('utf-8'))

    user = User(
        username=data.login,
        email=data.email,
        password=s.hexdigest(),
    )
    session.add(user)
    await session.flush()
    await session.refresh(user)

    encoded_token = jwt.encode({'username': data.login, 'password': data.password}, 'secret', algorithm="HS256")
    sess = Session(
        token=encoded_token,
        user_id=user.id,
        valid_datetime=datetime.datetime.now() + datetime.timedelta(days=31)
    )
    session.add(sess)
    await session.flush()
    await session.commit()

    return encoded_token

@router.post('/login')
async def user_login(
    data: UserLoginData,
    session: AsyncSession = Depends(get_pgsql_session),
):
    user = (
        await session.execute(
            select(User)
            .where(
                User.username == data.login,
                User.password == hashlib.md5(data.password.encode('utf-8')).hexdigest()
            )
        )
    ).scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не зарегистрирован')

    user_session = (await session.execute(select(Session).where(Session.user_id == user.id, Session.valid_datetime >= datetime.datetime.now()))).scalars().one_or_none()
    if user_session:
        print('we have session already')
        return user_session.token

    encoded_token = jwt.encode({'username': data.login, 'password': data.password}, 'secret', algorithm="HS256")
    sess = Session(
        token=encoded_token,
        user_id=user.id,
        valid_datetime=datetime.datetime.now() + datetime.timedelta(days=31)
    )
    session.add(sess)
    await session.flush()
    await session.commit()


@router.get('/me')
async def get_my_profile(
    request: Request,
    session: AsyncSession = Depends(get_pgsql_session),
):
    if not 'Authorization' in request.headers:
        raise HTTPException(status_code=400, detail='Не отправлен authorization token')

    token = request.headers['Authorization']
    user_session = (await session.execute(select(Session).where(Session.token==token))).scalars().one_or_none()
    if not user_session:
        raise HTTPException(status_code=400, detail='Отправлен неверный токен')

    user = (await session.execute(select(User).where(User.id == user_session.user_id))).scalars().one_or_none()

    if user:
        return UserEntity.model_validate(user, from_attributes=True)

    raise HTTPException(status_code=400, detail='Пользователь с данным id не найден')


@router.get('/list')
async def users_list(
    request: Request,
    session: AsyncSession = Depends(get_pgsql_session),
):
    users = (await session.execute(select(User))).scalars().all()
    return [ListUserEntity.model_validate(x, from_attributes=True) for x in users]