from typing import Annotated, Self

from fastapi import Depends

from api.v1 import protocols


class GetUserController:
    def __init__(self: Self) -> None:
        pass


    async def get_user():
        ...



async def user_controller() -> GetUserController:
    return GetUserController()


get_user_controller = Annotated[
    protocols.GetUserControllerProtocol,
    Depends(user_controller),
]
