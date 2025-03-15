from typing import Self

from fastapi import HTTPException, Request

from apps.auth.presentation import protocols as proto
from apps.auth.presentation.schemas.responses import RefreshAccessJwtResponse
from core.config import JwtType
from core.exceptions import BaseError
from core.schema import ApiResponse, Status


class RefreshController:
    def __init__(
            self: Self,
            refresh_jwt_usecase: proto.RefreshJwtUsecaseProtocol,
    ) -> None:
        self.refresh_uc = refresh_jwt_usecase


    async def refresh(
            self: Self,
            request: Request,
    ) -> ApiResponse[RefreshAccessJwtResponse, None]:
        try:
            refresh_token = request.cookies.get(JwtType.REFRESH.value)
            if not refresh_token:
                raise HTTPException(
                    status_code=401,
                    detail="Refresh token not found",
                )
            response = await self.refresh_uc.execute(refresh_token)
            return ApiResponse(
                status=Status.SUCCESS,
                data=RefreshAccessJwtResponse(
                    access_jwt=response.access_jwt,
                ),
            )
        except BaseError as e:
            raise HTTPException(  # noqa: B904
                status_code=e.status_code,
                detail=e.detail,
            )

