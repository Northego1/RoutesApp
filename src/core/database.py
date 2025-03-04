from contextlib import asynccontextmanager
from typing import AsyncGenerator, Self

from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


class DataBase:
    def __init__(self: Self, url: str) -> None:
        self.engine = create_async_engine(
            url=url,
            pool_size=settings.db.CONN_POOL,
            max_overflow=settings.db.MAX_OVERFLOW,
            pool_timeout=settings.db.TIMEOUT,
            pool_recycle=settings.db.CONN_RECYCLE,
        )


    async def get_ready_connection_pool(self: Self) -> None:
        for _ in range(settings.db.CONN_POOL):
            connect = await self.engine.connect()
            await connect.close()


    @asynccontextmanager
    async def connection(self: Self) -> AsyncGenerator[AsyncConnection, None]:
        async with self.engine.begin() as conn:
            yield conn


class Base(DeclarativeBase):
    pass
