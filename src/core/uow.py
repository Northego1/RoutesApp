import contextlib
import dataclasses
from typing import AsyncGenerator, Self

from sqlalchemy.ext.asyncio import AsyncConnection

from apps.auth.infrastructure.repositories.refresh_jwt_repository import RefreshJwtRepository
from apps.auth.infrastructure.repositories.user_repository import UserRepository
from core.database import DataBase


@dataclasses.dataclass(slots=True)
class Repository:
    _conn: AsyncConnection

    _user_repository: UserRepository | None = None
    _refresh_repository: RefreshJwtRepository | None = None


    @property
    def user_repository(self: Self) -> UserRepository:
        if not self._user_repository:
            self._user_repository = UserRepository(self._conn)
        return self._user_repository

    @property
    def refresh_repository(self: Self) -> RefreshJwtRepository:
        if not self._refresh_repository:
            self._refresh_repository = RefreshJwtRepository(self._conn)
        return self._refresh_repository


class UnitOfWork:
    def __init__(self, db: DataBase) -> None:
        self.db = db


    @contextlib.asynccontextmanager
    async def transaction(self: Self) -> AsyncGenerator[Repository, None]:
        conn = await self.db.engine.connect()
        conn.begin()
        try:
            yield Repository(conn)
        except Exception as e:
            raise e
            # await conn.rollback()
        else:
            await conn.commit()
        finally:
            await conn.aclose()


