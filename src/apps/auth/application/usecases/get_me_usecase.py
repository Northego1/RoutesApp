import uuid
from typing import Protocol, Self

from apps.auth.application import protocols as proto
from apps.auth.application.dto import UserDto
from apps.auth.domain.token import Token
from apps.auth.domain.user import User
from core.config import JwtType
from core.exceptions import BaseError


class UserRepositoryProtocol(Protocol):
        async def get_user_by_id(
            self: Self, user_id: uuid.UUID, with_tokens: bool = False,
    ) -> User | None: ...

class RefreshJwtRepositoryProtocol(Protocol):
    async def update(
            self: Self, older_token: Token, new_token: Token) -> None: ...
    async def insert(self: Self, refresh_jwt: Token) -> uuid.UUID | None: ...


class RepositoryProtocol(Protocol):
    user_repository: UserRepositoryProtocol
    refresh_repository: RefreshJwtRepositoryProtocol


class SecurityProtocol(Protocol):
    def decode_and_verify_jwt(self: Self,token: str) -> Token | None: ...


class GetMeUsecase:
    def __init__(
            self: Self,
            uow: proto.UowProtocol[RepositoryProtocol],
            security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security


    async def execute(self: Self, access_token: str) -> UserDto:
        access_jwt = self.security.decode_and_verify_jwt(access_token)
        if not access_jwt or access_jwt.type != JwtType.ACCESS:
            raise BaseError("invalid access token")

        async with self.uow.transaction() as repo:
            user = await repo.user_repository.get_user_by_id(access_jwt.user_id)

            if not user:
                raise BaseError("user not found")
            return UserDto(
                id=user.id,
                username=user.username,
                email=user.email,
            )









