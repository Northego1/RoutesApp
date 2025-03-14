
import uuid
from typing import Self, overload

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from apps.auth.domain.user import User


class UserRepository:
    def __init__(self: Self, conn: AsyncConnection) -> None:
        self.conn = conn

    async def _get_user_by_with_tokens(
            self: Self, parametr: str | uuid.UUID,
    ) -> User | None:
        param_name = "id" if isinstance(parametr, uuid.UUID) else "username"
        query = await self.conn.execute(
            text(
                f"""
                    SELECT us.*, json_agg(rj.*)
                    FROM users us
                    JOIN refresh_jwts rj
                    ON us.id = rj.user_id
                    WHERE us.{param_name} = :parametr
                    GROUP BY us.id;
                """,  # noqa: S608
            ),
            {
                "parametr": parametr,
            },
        )

        row = query.fetchone()
        if not row:
            return None
        return User(*row)


    async def _get_user_by(
            self: Self, parametr: str | uuid.UUID,
    ) -> User | None:
        param_name = "id" if isinstance(parametr, uuid.UUID) else "username"

        query = await self.conn.execute(
            text(
                f"""
                    SELECT *
                    FROM users
                    WHERE {param_name} = :parametr
                """,  # noqa: S608
            ),
            {
                "parametr": parametr,
            },
        )

        row = query.fetchone()
        if not row:
            return None
        return User(*row)

    @overload
    async def get_user(
        self: Self, *, user_id: uuid.UUID, with_tokens: bool = False,
    ) -> User | None: ...

    @overload
    async def get_user(
        self: Self, *, username: str, with_tokens: bool = False,
    ) -> User | None: ...


    async def get_user(
            self: Self,
            *,
            user_id: uuid.UUID | None = None,
            username: str | None = None,
            with_tokens: bool = False,
    ) -> User | None:
        if user_id:
            parametr = user_id
        elif username:
            parametr = username
        else:
            raise Exception
        if with_tokens:
            return await self._get_user_by_with_tokens(parametr=parametr)
        return await self._get_user_by(parametr=parametr)


    async def create_user(self: Self, user: User) -> None | uuid.UUID:
        query = await self.conn.execute(
            text(
                """
                    INSERT INTO users (id, username, email, password)
                    VALUES (:user_id, :username, :email, :password)
                    ON CONFLICT (username) DO NOTHING
                    RETURNING id;
                """,
            ),
            {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "password": user.password,
            },
        )

        return query.scalar()


    async def update_user(self: Self, user: User) -> None:
        await self.conn.execute(
            text(
                """
                    UPDATE users
                    SET
                        username = :username,
                        email = :email,
                        password = :password
                    WHERE id = :user_id
                """,
            ),
            {
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "user_id": user.id,
            },
        )
