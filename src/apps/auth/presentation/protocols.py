from typing import Protocol, Self

from apps.auth.application import dto


class GetUserUsecaseProtocol(Protocol):
    async def execute(self: Self, access_token: str) -> dto.UserDto: ...

class LoginUsecaseProtocol(Protocol):
    async def execute(
            self: Self, password: str, username: str,
    ) -> dto.UserLoginDto: ...

class LogoutUsecaseProtocol(Protocol):
    async def execute(self: Self) -> None: ...

class RefreshJwtUsecaseProtocol(Protocol):
    async def execute(self: Self, refresh_jwt: str) -> dto.RefreshJwtDto: ...

class RegisterUsecaseProtocol(Protocol):
    async def execute(
            self: Self,
            username: str,
            password: str,
            email: str | None = None,
    ) -> dto.UserRegisterDto: ...

class UpdateUsecaseProtocol(Protocol):
    async def execute(self: Self) -> None: ...



