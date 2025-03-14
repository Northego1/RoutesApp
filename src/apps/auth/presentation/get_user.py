from typing import Self

from fastapi import Request

from apps.auth.presentation import protocols as proto
from core.exceptions import BaseError


class GetUserController:
    def __init__(
            self: Self,
            get_user_usecase: proto.GetUserUsecaseProtocol,
    ) -> None:
        self.get_user_uc = get_user_usecase


    async def get_user():
        ...



async def get_user_usecase(request: Request):
    access_token_header = request.headers.get("Authorization")
    if not access_token_header:
        raise BaseError
    access_token = access_token_header.split()[1]
    


