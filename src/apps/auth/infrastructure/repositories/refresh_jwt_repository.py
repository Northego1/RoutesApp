import uuid
from typing import Self

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from apps.auth.domain.refresh_jwt import RefreshJwt


class RefreshJwtRepository:
    def __init__(self: Self, conn: AsyncConnection) -> None:
        self.conn = conn


    async def update(
            self: Self,
            older_token: RefreshJwt,
            new_token: RefreshJwt,
    )-> None | uuid.UUID:
        query = await self.conn.execute(
            text(
                """
                    UPDATE refresh_jwts
                    SET
                        id = :jti
                        user_id = :user_id,
                        token = :token,
                        token_expire = :token_expire
                    WHERE id = :old_jti
                    RETURNING id
                """,
            ),
            {
                "jti": new_token.id,
                "user_id": new_token.user_id,
                "token": new_token.token,
                "token_expire": new_token.token_expire,
                "old_jti": older_token.id,
            },
        )

        return query.scalar()


    async def insert(self: Self, refresh_jwt: RefreshJwt) -> uuid.UUID | None:
        query = await self.conn.execute(
            text(
                """
                    INSERT INTO refresh_jwts (id, user_id, token, token_expire)
                    VALUES (:id, :user_id, :token, :token_expire)
                    RETURNING id;
                """,
            ),
            {
                "id": refresh_jwt.id,
                "user_id": refresh_jwt.user_id,
                "token": refresh_jwt.token,
                "token_expire": refresh_jwt.token_expire,
            },
        )

        return query.scalar()
