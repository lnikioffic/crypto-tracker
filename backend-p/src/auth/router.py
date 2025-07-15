from typing import Annotated
import logging
from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPBearer
from src.auth.config import auth_jwt_settings
from src.auth.dependencies import (
    get_current_auth_user_by_token_sub,
    get_current_auth_user_for_refresh,
    refresh_token_jwt,
    validate_auth_user_issue_jwt,
    validate_create_user,
)
from src.auth.schemas import TokenInfo, UserCreate, UserRead
from src.auth.service import create_user
from src.database import DbSession

log = logging.getLogger(__name__)

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
    response: Response,
    token: Annotated[TokenInfo, Depends(validate_auth_user_issue_jwt)],
):
    response.set_cookie(
        key='access_token',
        value=token.access_token,
        httponly=True,
        max_age=auth_jwt_settings.access_token_expire_minutes * 60,
    )
    response.set_cookie(
        key='refresh_token',
        value=token.refresh_token,
        httponly=True,
        max_age=auth_jwt_settings.refresh_token_expire_days * 24 * 60 * 60,
    )
    return token


@auth_router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')
    return TokenInfo(access_token='', refresh_token='')


@auth_router.post(
    '/refresh', response_model=TokenInfo, response_model_exclude_none=True
)
async def refresh(
    response: Response,
    user: Annotated[UserRead, Depends(get_current_auth_user_for_refresh)],
):
    token = await refresh_token_jwt(user)
    response.set_cookie(
        key='access_token',
        value=token.access_token,
        httponly=True,
        max_age=auth_jwt_settings.access_token_expire_minutes * 60,
    )
    return token


@user_router.get('/me', response_model=UserRead)
async def get_current_user(
    user: Annotated[UserRead, Depends(get_current_auth_user_by_token_sub)],
):
    return user
