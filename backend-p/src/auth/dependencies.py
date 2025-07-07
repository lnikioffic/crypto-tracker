from typing import Annotated

from fastapi import Depends, Form, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas import TokenInfo, UserLogin, UserRead
from src.auth.service import get_user_by_id, get_user_by_username
from src.auth.token import (
    TOKEN_TYPE_FIELD,
    TokenType,
    create_access_token,
    create_refresh_token,
)
from src.auth.utils import decode_jwt, validate_password
from src.database import DbSession

error_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='User not found',
)


async def create_token_jwt(user: UserRead) -> TokenInfo:
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


async def refresh_token_jwt(user: UserRead) -> TokenInfo:
    access_token = await create_access_token(user)

    return TokenInfo(access_token=access_token)


async def valid_user_username(user_name: str, session: AsyncSession) -> UserLogin:
    user = await get_user_by_username(session, user_name)

    if not user:
        raise error_found

    return user


async def valid_user_id(
    user_id: Annotated[int, Path], session: AsyncSession
) -> UserRead | None:
    user = await get_user_by_id(session, user_id)

    if not user:
        raise error_found

    return user


async def validate_create_user(
    user: UserRead,
) -> TokenInfo:

    return await create_token_jwt(user)


async def validate_auth_user_issue_jwt(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: DbSession,
) -> TokenInfo:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid username or password',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    user: UserLogin = await valid_user_username(username, session)
    if not user:
        raise unauthed_exc

    if not validate_password(
        password=password,
        hash_password=user.password,
    ):
        raise unauthed_exc

    return await create_token_jwt(user)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_current_token_payload(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> dict:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from err
    return payload


async def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'invalid token type {current_token_type!r} expected {token_type!r}',
    )


async def get_current_auth_user_by_token_sub(
    session: DbSession,
    payload: Annotated[dict, Depends(get_current_token_payload)],
) -> UserRead:
    await validate_token_type(payload=payload, token_type=TokenType.ACCESS_TOKEN_TYPE)
    id: str | None = payload.get('sub')
    if user := await valid_user_id(int(id), session):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='token invalid (user not found)',
    )


async def get_current_auth_user_for_refresh(
    session: DbSession,
    payload: Annotated[dict, Depends(get_current_token_payload)],
) -> UserRead:
    await validate_token_type(payload=payload, token_type=TokenType.REFRESH_TOKEN_TYPE)
    id: str | None = payload.get('sub')
    if user := await valid_user_id(int(id), session):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='token invalid (user not found)',
    )
