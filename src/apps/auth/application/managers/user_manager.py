import uuid
from typing import Protocol, Self, overload

from apps.auth.domain.user import User
from core.exceptions import BaseError


class UserRepositoryProtocol(Protocol):
    async def get_user(
            self: Self,
            *,
            user_id: uuid.UUID | None = None,
            username: str | None = None,
            with_tokens: bool = False,
    ) -> User | None: ...

class RepositoryProtocol(Protocol):
    user_repository: UserRepositoryProtocol

class SecurityProtocol(Protocol):
    def check_password(self: Self, correct_password: bytes, checkable_password: bytes) -> bool: ...


class UserManager:
    def __init__(
            self: Self,
            security: SecurityProtocol,
    ) -> None:
        self.security = security


    @overload
    async def get_user(
        self: Self, repository: RepositoryProtocol, *, user_id: uuid.UUID,
    ) -> User: ...
    @overload
    async def get_user(
        self: Self, repository: RepositoryProtocol, *, username: str,
    ) -> User: ...

    async def get_user(
            self: Self,
            repository: RepositoryProtocol,
            *,
            user_id: uuid.UUID | None = None,
            username: str | None = None,
    ) -> User:
        if username:
            user = await repository.user_repository.get_user(username=username)
        elif user_id:
            user = await repository.user_repository.get_user(user_id=user_id)
        else:
            raise Exception
        if not user:
            raise BaseError
        return user


    @overload
    async def autentificate(
        self: Self, repository: RepositoryProtocol, *,
        user_id: uuid.UUID, password: str) -> None: ...
    @overload
    async def autentificate(
        self: Self, repository: RepositoryProtocol, *,
        username: str, password: str) -> None: ...

    async def autentificate(
            self: Self,
            repository: RepositoryProtocol,
            *,
            user_id: uuid.UUID | None = None,
            username: str | None = None,
            password: str,
    ) -> None:
        if user_id:
            user = await self.get_user(repository, user_id=user_id)
        elif username:
            user = await self.get_user(repository, username=username)
        else:
            raise Exception
        

