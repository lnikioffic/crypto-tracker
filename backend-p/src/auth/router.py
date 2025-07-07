from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from src.auth.dependencies import (
    get_current_auth_user_by_token_sub,
    validate_auth_user_issue_jwt,
    validate_create_user,
    get_current_auth_user_for_refresh,
    refresh_token_jwt,
)
from src.auth.schemas import TokenInfo, UserCreate, UserRead
from src.auth.service import create_user
from src.auth.token import create_refresh_token
from src.database import DbSession

http_bearer = HTTPBearer(auto_error=False)
auth_router = APIRouter(
    prefix='/auth', tags=['Auth'], dependencies=[Depends(http_bearer)]
)
user_router = APIRouter(
    prefix='/user', tags=['User'], dependencies=[Depends(http_bearer)]
)


@auth_router.post(
    '/register', status_code=status.HTTP_201_CREATED, response_model=TokenInfo
)
async def register(user: UserCreate, session: DbSession):
    user_read = await create_user(session, user)
    token = await validate_create_user(user_read)
    return token


@auth_router.post('/login', response_model=TokenInfo)
async def login(
    token: Annotated[TokenInfo, Depends(validate_auth_user_issue_jwt)],
):
    return token


@auth_router.post('/logout')
async def logout():
    return TokenInfo(access_token='', refresh_token='')


@auth_router.post(
    '/refresh', response_model=TokenInfo, response_model_exclude_none=True
)
async def refresh(
    user: Annotated[UserRead, Depends(get_current_auth_user_for_refresh)],
):
    token = await refresh_token_jwt(user)
    return token


@user_router.get('/me', response_model=UserRead)
async def get_current_user(
    user: Annotated[UserRead, Depends(get_current_auth_user_by_token_sub)],
):
    return user
