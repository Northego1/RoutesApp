
import uuid
from typing import Self

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from apps.auth.domain.token import Token
from apps.auth.domain.user import User


class UserRepository:
    def __init__(self: Self, conn: AsyncConnection) -> None:
        self.conn = conn


    async def get_user_by_id(
            self: Self, user_id: uuid.UUID, with_tokens: bool = False,
    ) -> User | None:
        if with_tokens:
            query = await self.conn.execute(
                text(
                    """
                    SELECT us.*, json_agg(rj.*)
                    FROM users us
                    JOIN refresh_jwts rj
                    ON us.id = rj.user_id
                    WHERE us.id = :user_id
                    GROUP BY us.id;
                    """,
                ),
                {
                    "username": user_id,
                },
            )
        else:
            query = await self.conn.execute(
                text(
                    """
                        SELECT *
                        FROM users
                        WHERE id = :user_id
                    """,
                ),
                {
                    "user_id": user_id,
                },
            )
        row = query.fetchone()
        if not row:
            return None
        return User(*row)


    async def get_user_by_username(
            self: Self, username: str, with_tokens: bool = False,
    ) -> User | None:
        if with_tokens:
            query = await self.conn.execute(
                text(
                    """
                    SELECT us.*, json_agg(rj.*)
                    FROM users us
                    JOIN refresh_jwts rj
                    ON us.id = rj.user_id
                    WHERE us.username = :username
                    GROUP BY us.id;
                    """,
                ),
                {
                    "username": username,
                },
            )
            row = query.fetchone()
            if not row:
                return None
            row_dict = row._asdict()
            jwts_list = [Token(**el) for el in row_dict.pop("json_agg")]
            return User(token_list=jwts_list, **row_dict)
        else:
            query = await self.conn.execute(
                text(
                    """
                        SELECT *
                        FROM users
                        WHERE username = :username
                    """,
                ),
                {
                    "username": username,
                },
            )

            row = query.fetchone()
            if not row:
                return None
            return User(*row)


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
