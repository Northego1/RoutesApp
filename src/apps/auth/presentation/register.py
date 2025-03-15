from typing import Self

from fastapi import HTTPException, Response

from apps.auth.presentation import protocols as proto
from apps.auth.presentation.schemas.requests import RegisterRequest
from apps.auth.presentation.schemas.responses import RegisterResponse
from core.config import JwtType, settings
from core.exceptions import BaseError
from core.schema import ApiResponse, Status


class RegisterController:
    def __init__(
            self: Self,
            register_usecase: proto.RegisterUsecaseProtocol,
    ) -> None:
        self.register_uc = register_usecase

    async def register(
            self: Self,
            response: Response,
            register_request: RegisterRequest,
    ) -> ApiResponse[RegisterResponse, None]:
        try:
            login_dto = await self.register_uc.execute(
                username=register_request.username,
                password=register_request.password,
                email=register_request.email,
            )
            response.set_cookie(
                JwtType.REFRESH.value,
                login_dto.refresh_jwt,
                httponly=True,
                samesite="strict",
                max_age=settings.jwt.REFRESH_JWT_EXPIRE * 60,
            )
            return ApiResponse(
                status=Status.SUCCESS,
                data=RegisterResponse(
                    username=login_dto.username,
                    access_jwt=login_dto.access_jwt,
                ),
            )
        except BaseError as e:
            raise HTTPException(  # noqa: B904
                status_code=e.status_code,
                detail=e.detail,
            )



