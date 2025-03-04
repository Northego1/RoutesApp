from typing import Annotated, Self

from fastapi import Depends

from api.v1 import protocols


class UpdateUserController:
    def __init__(self: Self) -> None:
        ...

    async def update_user(self: Self):
        ...



async def get_update_controller() -> UpdateUserController:
    return UpdateUserController()


update_controller = Annotated[
    protocols.UpdateUserControllerProtocol,
    Depends(get_update_controller)
]