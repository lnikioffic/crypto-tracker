from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from src.auth.config import auth_jwt_settings


def encode_jwt(
    payload: dict,
    private_key: str = auth_jwt_settings.private_key_path.read_text(),
    algorithm: str = auth_jwt_settings.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = auth_jwt_settings.access_token_expire_minutes,
):
    to_encode = payload.copy()
    now = datetime.now(UTC)
    
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        iat=now,
        exp=expire,
    )
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = auth_jwt_settings.public_key_path.read_text(),
    algorithm: str = auth_jwt_settings.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode(),
    )
