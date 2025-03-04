from typing import Annotated, Self

from fastapi import Depends

from api.v1 import protocols


class RefreshController:
    def __init__(self) -> None:
        pass


    async def refresh(self: Self):
        ...



async def get_refresh_controller() -> RefreshController:
    return RefreshController()


refresh_controller = Annotated[
    protocols.RefreshJwtControllerProtocol,
    Depends(get_refresh_controller),
]
