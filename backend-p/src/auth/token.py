from datetime import timedelta
from enum import StrEnum

from src.auth.config import auth_jwt_settings
from src.auth.schemas import UserRead
from src.auth.utils import encode_jwt

TOKEN_TYPE_FIELD = 'type'


class TokenType(StrEnum):
    ACCESS_TOKEN_TYPE = 'access'
    REFRESH_TOKEN_TYPE = 'refresh'


async def create_token(
    token_type: str,
    payload: dict,
    expire_minutes: int = auth_jwt_settings.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:

    jwt_payload = {TOKEN_TYPE_FIELD: token_type}

    jwt_payload.update(payload)

    token = encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )
    return token


async def create_access_token(user: UserRead) -> str:
    payload = {
        'sub': str(user.id),
        'user': {
            'username': user.username,
            'email': user.email,
        },
    }

    return await create_token(
        token_type=TokenType.ACCESS_TOKEN_TYPE,
        payload=payload,
        expire_minutes=auth_jwt_settings.access_token_expire_minutes,
    )


async def create_refresh_token(user: UserRead) -> str:
    payload = {
        'sub': str(user.id),
    }

    return await create_token(
        token_type=TokenType.REFRESH_TOKEN_TYPE,
        payload=payload,
        expire_timedelta=timedelta(days=auth_jwt_settings.refresh_token_expire_days),
    )
