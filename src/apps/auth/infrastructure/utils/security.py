import uuid
from datetime import UTC, datetime, timedelta
from typing import Any, Self

import bcrypt
import jwt

from apps.auth.domain.token import Token
from apps.auth.domain.user import User
from core.config import JwtType, settings


class Security:
    def create_jwt(
            self: Self,
            user: User,
            jwt_type: JwtType,
            refresh_jti: uuid.UUID | None = None,
            **kwargs: Any,
    ) -> Token:
        """creating jwt token, extending jti, token_type, expire"""
        expire = settings.jwt.ACCESS_JWT_EXPIRE \
        if jwt_type == JwtType.ACCESS else settings.jwt.REFRESH_JWT_EXPIRE

        expire_at = (datetime.now(UTC) + timedelta(minutes=expire))
        jti = uuid.uuid4()
        payload = {
            "user_id": str(user.id),
            "username": user.username,
            "type": jwt_type.value,
            "jti": str(jti),
            "exp": expire_at.timestamp(),
        }
        if refresh_jti:
            payload["refresh_jti"] = str(refresh_jti)
        if kwargs:
            payload.update(kwargs)

        token = jwt.encode(
            payload=payload,
            key=settings.jwt.PRIVATE_KEY,
            algorithm=settings.jwt.ALGORITHM,
        )
        return Token(
            id=payload["jti"],
            user_id=payload["user_id"],
            token=token,
            token_expire=expire_at,
            type=jwt_type,
        )


    def decode_and_verify_jwt(self: Self, token: str) -> Token | None:
        """ returns None if token is invalid"""
        try:
            payload = jwt.decode(
                token,
                key=settings.jwt.PUBLIC_KEY,
                algorithms=[settings.jwt.ALGORITHM],
            )
            return Token(
                id=payload["jti"],
                user_id=payload["user_id"],
                token=token,
                token_expire=datetime.fromtimestamp(int(payload["exp"]), tz=UTC),
                type=payload["type"],
            )
        except jwt.exceptions.PyJWTError:
            return None


    def hash_password(
            self: Self,
            password: str,
    ) -> bytes:
        return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt(),
        )

    def check_password(
            self: Self,
            correct_password: bytes,
            checkable_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            checkable_password,
            correct_password,
        )
