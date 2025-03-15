from typing import Self

from fastapi import HTTPException, Response

from apps.auth.presentation import protocols as proto
from apps.auth.presentation.schemas.requests import LoginRequest
from apps.auth.presentation.schemas.responses import LoginResponse
from core.config import JwtType, settings
from core.exceptions import BaseError
from core.schema import ApiResponse, Status


class LoginController:
    def __init__(
            self: Self,
            login_usecase: proto.LoginUsecaseProtocol,
    ) -> None:
        self.login_uc = login_usecase


    async def login(
            self: Self,
            response: Response,
            login_request: LoginRequest,
    ) -> ApiResponse[LoginResponse, None]:
        try:
            login_dto = await self.login_uc.execute(
                username=login_request.username,
                password=login_request.password,
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
                data=LoginResponse(
                    access_jwt=login_dto.access_jwt,
                ),
            )
        except BaseError as e:
            raise HTTPException(  # noqa: B904
                status_code=e.status_code,
                detail=e.detail,
            )


