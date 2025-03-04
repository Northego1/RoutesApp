import contextlib
import dataclasses
from typing import AsyncGenerator, Protocol, Self

from core.database import DataBase


class SessionProtocol(Protocol):
    async def commit(self: Self) -> None: ...
    async def rollback(self: Self) -> None: ...
    async def close(self: Self) -> None: ...


@dataclasses.dataclass(slots=True)
class Repository:
    _conn: SessionProtocol
    # _notifications: Notifications | None = None
    # _owners: Owners | None = None


    # @property
    # def notifications(self: Self) -> Notifications:
    #     if self._notifications is None:
    #         self._notifications = Notifications()
    #     return self._notifications

    # @property
    # def owners(self: Self) -> Owners:
    #     if self._owners is None:
    #         self._owners = Owners()
    #     return self._owners


class UnitOfWork:
    def __init__(self, db: DataBase) -> None:
        self.db = db


    @contextlib.asynccontextmanager
    async def transaction(self: Self) -> AsyncGenerator[Repository, None]:
        conn = await self.db.engine.connect()
        conn.begin()
        try:
            yield Repository(conn)
        except Exception:
            await conn.rollback()
        else:
            await conn.commit()
        finally:
            await conn.aclose()

