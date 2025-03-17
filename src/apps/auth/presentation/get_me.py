import uuid
from typing import Self

from fastapi import HTTPException, Request

from apps.auth.presentation import protocols as proto
from apps.auth.presentation.schemas.responses import GetMeResponse
from core.exceptions import BaseError
from core.schema import ApiResponse, Status


class GetMeController:
    def __init__(
            self: Self,
            get_user_usecase: proto.GetUserUsecaseProtocol,
    ) -> None:
        self.get_user_uc = get_user_usecase


    async def get_me(self: Self, request: Request, api_response: bool = True,
    ) -> ApiResponse[GetMeResponse, None] | GetMeResponse:
        try:
            token_header = request.headers.get("Authorization")
            if not token_header:
                raise HTTPException(
                    status_code=401,
                    detail="Unauthorized",
                )
            token = token_header.split()
            if len(token) != 2 or token[0] != "Bearer":
                raise HTTPException(
                    status_code=401,
                    detail="Unauthorized",
                )
            token = token[1]
            user_dto = await self.get_user_uc.execute(token)

            resp_data = GetMeResponse(
                    id=user_dto.id,
                    email=user_dto.email,
                    username=user_dto.username,
                )
            if api_response:
                return ApiResponse(
                    status=Status.SUCCESS,
                    data=resp_data,
                )
            return resp_data

        except BaseError as e:
            raise HTTPException(  # noqa: B904
                status_code=e.status_code,
                detail=e.detail,
            )





