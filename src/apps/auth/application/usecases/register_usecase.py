import uuid
from typing import Any, Protocol, Self

from apps.auth.application import protocols as proto
from apps.auth.application.dto import UserRegisterDto
from apps.auth.domain.refresh_jwt import RefreshJwt
from apps.auth.domain.user import User
from core.config import JwtType
from core.exceptions import BaseError


class UserExistsError(BaseError): ...

class UserRepositoryProtocol(Protocol):
    async def create_user(self: Self, user: User) -> None | uuid.UUID: ...


class RefreshRepositoryProtocol(Protocol):
    async def insert(self: Self, refresh_jwt: RefreshJwt) -> uuid.UUID | None: ...


class RepositoryProtocol(Protocol):
    user_repository: UserRepositoryProtocol
    refresh_repository: RefreshRepositoryProtocol


class SecurityProtocol(Protocol):
    def create_jwt(self: Self, user: User, jwt_type: str) -> RefreshJwt: ...


class RegisterUsecase:
    def __init__(
            self: Self,
            uow: proto.UowProtocol[RepositoryProtocol],
            security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security


    async def execute(
            self: Self,
            username: str,
            password: str,
            email: str | None = None,
    ) -> UserRegisterDto:
        user = User(
            id=uuid.uuid4(),
            username=username,
            password=password,
            email=email,
        )
        async with self.uow.transaction() as repo:
            user_id = await repo.user_repository.create_user(user=user)
            if not user_id:
                raise UserExistsError("User already exists", status_code=401)

            refresh_jwt = self.security.create_jwt(user=user, jwt_type=JwtType.REFRESH)
            refresh_id = await repo.refresh_repository.insert(refresh_jwt)
            if not refresh_id:
                raise BaseError("Unkown Error", status_code=401)

            access_jwt = self.security.create_jwt(user=user, jwt_type=JwtType.ACCESS)

            return UserRegisterDto(
                username=username,
                refresh_jwt=refresh_jwt.token,
                access_jwt=access_jwt.token,
            )

