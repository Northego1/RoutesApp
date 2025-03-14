import uuid
from typing import Protocol, Self

from apps.auth.application import protocols as proto
from apps.auth.application.dto import UserLoginDto
from apps.auth.domain.refresh_jwt import RefreshJwt
from apps.auth.domain.user import User
from core.config import JwtType
from core.exceptions import BaseError


class UserRepositoryProtocol(Protocol):
    async def get_user_with_tokens(self: Self, username: str) -> User | None: ...

class RefreshJwtRepositoryProtocol(Protocol):
    async def update(
            self: Self, older_token: RefreshJwt, new_token: RefreshJwt) -> None: ...
    async def insert(self: Self, refresh_jwt: RefreshJwt) -> uuid.UUID | None: ...


class RepositoryProtocol(Protocol):
    user_repository: UserRepositoryProtocol
    refresh_repository: RefreshJwtRepositoryProtocol


class SecurityProtocol(Protocol):
    def create_jwt(self: Self, user: User, jwt_type: str) -> RefreshJwt: ...
    def check_password(self: Self, correct_password: bytes, checkable_password: bytes) -> bool: ...


class LoginUsecase:
    def __init__(
            self: Self,
            uow: proto.UowProtocol[RepositoryProtocol],
            security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security


    async def execute(
            self: Self,
            password: str,
            username: str,
    ) -> UserLoginDto:
        """
            Login usecase accepting username and password,
            usecase takes user from db, checks password,
            creating tokens and returns dto with tokens
        """
        async with self.uow.transaction() as repo:
            user = await repo.user_repository.get_user_with_tokens(username)

            if not user:
                raise BaseError(detail="UserNotFound", status_code=404)
            if not self.security.check_password(user.password, password.encode()):
                raise BaseError(detail="Username or password is incorrect", status_code=401)

            refresh_jwt = self.security.create_jwt(user, jwt_type=JwtType.REFRESH)
            older_token = user.swapsert_jwt(refresh_jwt)

            if older_token:
                result = await repo.refresh_repository.update(older_token, refresh_jwt)
            else:
                result = await repo.refresh_repository.insert(refresh_jwt)
            if not result:
                raise BaseError(detail="UknownError", status_code=401)

            access_jwt = self.security.create_jwt(user, jwt_type=JwtType.ACCESS)

            return UserLoginDto(
                refresh_jwt=refresh_jwt.token,
                access_jwt=access_jwt.token,
            )







