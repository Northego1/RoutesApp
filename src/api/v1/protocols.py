import uuid
from typing import Protocol, Self

from fastapi import Request, Response

from apps.auth.presentation.schemas import requests as req
from apps.auth.presentation.schemas import responses as resp
from core.schema import ApiResponse as ApiResp


class GetUserControllerProtocol(Protocol):
    async def get_me(
            self: Self, request: Request,
    ) -> ApiResp[resp.GetMeResponse, None]: ...


class LoginControllerProtocol(Protocol):
    async def login(
            self: Self,
            response: Response,
            request_data: req.LoginRequest,
    ) -> ApiResp[resp.LoginResponse, None]: ...


class LogoutControllerProtocol(Protocol):
    async def logout(self: Self) -> None: ...


class RegisterControllerProtocol(Protocol):
    async def register(
            self: Self,
            response: Response,
            register_request: req.RegisterRequest,
    ) -> ApiResp[resp.RegisterResponse, None]: ...


class UpdateControllerProtocol(Protocol):
    async def update_user(
            self: Self,
            user_id: uuid.UUID,
            request_data: req.UpdateUserRequest,
    ) -> None: ...


class RefreshJwtControllerProtocol(Protocol):
    async def refresh(
            self: Self,
            request: Request,
    ) -> ApiResp[resp.RefreshAccessJwtResponse, None]: ...
