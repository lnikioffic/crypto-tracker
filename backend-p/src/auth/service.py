from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.auth.schemas import UserCreate, UserLogin, UserRead
from src.auth.utils import hash_password


async def get_user_by_username(
    session: AsyncSession, username: str
) -> UserLogin | None:
    stmt = select(User).filter(User.username == username)
    result: Result = await session.execute(stmt)
    user = result.scalar()
    return user


async def get_user_by_id(session: AsyncSession, id: int) -> User | None:
    user = await session.get(User, id)
    return user


async def get_user_by_email(session: AsyncSession, email: EmailStr) -> UserLogin | None:
    stmt = select(User).filter(User.email == email)
    result = await session.execute(stmt)
    user = result.scalar()
    return user


async def create_user(session: AsyncSession, user: UserCreate) -> UserRead:

    email_exist = await get_user_by_email(session, user.email)
    username_exist = await get_user_by_username(session, user.username)

    if email_exist is not None or username_exist is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email or username already exist',
        )

    user.password = hash_password(user.password).decode()
    add_user = User(**user.model_dump())
    session.add(add_user)
    await session.commit()
    return add_user
