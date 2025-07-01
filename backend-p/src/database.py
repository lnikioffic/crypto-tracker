import contextlib
from collections.abc import AsyncGenerator, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.config import settings


class DataBase:
    def __init__(self, db_url: str, echo: bool = False):
        self._engine: AsyncEngine = create_async_engine(url=db_url, echo=echo)
        self._sessionmaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        if self._engine is None:
            return
        await self._engine.dispose()

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise OSError("Session if not initialized")
        async with self._sessionmaker() as session:
            try:
                yield session

            except Exception:
                await session.rollback()
                raise

    async def connect(self) -> AsyncIterator[AsyncConnection]:
        pass


db = DataBase(settings.get_db_url())


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with db.session() as session:
        yield session
