from collections.abc import AsyncGenerator
from typing import Any

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import DataBase, get_session
from src.models import Base

TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test_db.db"


@pytest.fixture
async def database() -> AsyncGenerator[DataBase, None]:
    # Инициализируем базу данных для тестов
    db = DataBase(db_url=TEST_SQLALCHEMY_DATABASE_URL, echo=False)

    # Создаем таблицы
    async with db.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield db

    # Удаляем таблицы после тестов
    async with db.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Закрываем соединения
    await db.close()


@pytest.fixture
async def app():
    from src.main import app

    yield app


@pytest.fixture
async def db_session(database: DataBase) -> AsyncGenerator[AsyncSession, Any]:
    async with database.session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@pytest.fixture
async def client(
    app: FastAPI, db_session: AsyncSession
) -> AsyncGenerator[AsyncClient, Any]:
    async def _get_test_db():
        yield db_session

    app.dependency_overrides[get_session] = _get_test_db

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides = {}
