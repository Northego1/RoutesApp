import uuid
from typing import Any, Protocol, Self

from apps.auth.application import protocols as proto
from apps.auth.application.dto import RefreshJwtDto
from apps.auth.domain.token import Token
from apps.auth.domain.user import User
from core.config import JwtType
from core.exceptions import BaseError


class UserRepositoryProtocol(Protocol):
    async def get_user_by_id(
            self: Self, user_id: uuid.UUID, with_tokens: bool = False,
    ) -> User | None: ...

class RepositoryProtocol(Protocol):
    user_repository: UserRepositoryProtocol


class SecurityProtocol(Protocol):
    def create_jwt(self: Self, user: User, jwt_type: JwtType) -> Token: ...
    def decode_and_verify_jwt(self: Self, token: str) -> Token | None: ...


class RefreshJwtUsecase:
    def __init__(
            self: Self,
            uow: proto.UowProtocol[RepositoryProtocol],
            security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security


    async def execute(
            self: Self,
            refresh_jwt: str,
    ) -> RefreshJwtDto:
        refresh_jwt_entity = self.security.decode_and_verify_jwt(refresh_jwt)

        if not refresh_jwt_entity or refresh_jwt_entity.type != JwtType.REFRESH:
            raise BaseError(
                status_code=403,
                detail="Invalid refresh token",
            )
        async with self.uow.transaction() as repo:
            user = await repo.user_repository.get_user_by_id(refresh_jwt_entity.user_id)
            if not user:
                raise BaseError(
                    status_code=401,
                    detail="User not found",
                )
            access_jwt_entity = self.security.create_jwt(user, JwtType.ACCESS)
            return RefreshJwtDto(access_jwt=access_jwt_entity.token)






