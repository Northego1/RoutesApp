from typing import Self

from fastapi import HTTPException, Request

from apps.auth.presentation import protocols as proto
from core.config import JwtType
from core.exceptions import BaseError


class LogoutController:
    def __init__(
            self: Self,
            logout_usecase: proto.LogoutUsecaseProtocol,
    ) -> None:
        self.logout_uc = logout_usecase


    async def logout(self: Self, request: Request) -> None:
        access_jwt = None
        refresh_jwt = None
        try:
            token_header = request.headers.get("Authorization")
            if token_header:
                access_token = token_header.split()
                if len(access_token) == 2 or access_token[0] == "Bearer":
                    access_jwt = access_token[1]
            refresh_jwt = request.cookies.get(JwtType.REFRESH.value)

            await self.logout_uc.execute(access_token=access_jwt, refresh_token=refresh_jwt)
        except BaseError as e:
            raise HTTPException(  # noqa: B904
                status_code=e.status_code,
            )

