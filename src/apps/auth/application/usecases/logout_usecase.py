import uuid
from typing import Protocol, Self

from apps.auth.application import protocols as proto
from apps.auth.domain.token import Token
from core.config import JwtType
from core.exceptions import BaseError


class RefreshJwtRepositoryProtocol(Protocol):
    async def delete(self: Self, refresh_jwt_jti: uuid.UUID) -> uuid.UUID | None: ...


class RepositoryProtocol(Protocol):
    refresh_repository: RefreshJwtRepositoryProtocol


class SecurityProtocol(Protocol):
    def decode_and_verify_jwt(self: Self, token: str) -> Token | None: ...


class LogoutUsecase:
    def __init__(
            self: Self,
            uow: proto.UowProtocol[RepositoryProtocol],
            security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security


    async def execute(
            self: Self,
            refresh_token: str | None,
            access_token: str | None,
    ) -> None:
        delete_id = None

        if refresh_token:
            refresh_jwt = self.security.decode_and_verify_jwt(refresh_token)
            if refresh_jwt and refresh_jwt.type == JwtType.REFRESH:
                delete_id = refresh_jwt.id
        if not delete_id and access_token:
            access_jwt = self.security.decode_and_verify_jwt(access_token)
            if access_jwt and access_jwt.type == JwtType.ACCESS:
                delete_id = access_jwt.refresh_jti
        if not delete_id:
            raise BaseError(status_code=204)
        async with self.uow.transaction() as repo:
            print(f"{delete_id=}")
            result = await repo.refresh_repository.delete(delete_id)
            if not result:
                raise BaseError(status_code=204)




