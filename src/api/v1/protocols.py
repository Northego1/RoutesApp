import uuid
from typing import Protocol, Self

from apps.auth.presentation.schemas import responses as resp
from core.schema import ApiResponse as ApiResp


class GetUserControllerProtocol(Protocol):
    async def get_user(self: Self, user_id: uuid.UUID) -> ApiResp[resp.GetUserResponse, None]: ...

class LoginUserControllerProtocol(Protocol):
    async def login(self: Self) -> ApiResp[resp.LoginResponse, None]: ...

class LogoutUserControllerProtocol(Protocol):
    async def logout(self: Self): ...

class RegisterUserControllerProtocol(Protocol):
    async def register(self: Self) -> ApiResp[resp.RegisterResponse, None]: ...

class UpdateUserControllerProtocol(Protocol):
    async def update_user(self: Self): ...

class RefreshJwtControllerProtocol(Protocol):
    async def refresh(self: Self) -> ApiResp[resp.RefreshAccessJwtResponse, None]: ...
