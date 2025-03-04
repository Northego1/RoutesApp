from typing import Annotated, Self

from fastapi import Depends

from api.v1 import protocols


class LogoutController:
    def __init__(self) -> None:
        pass


    async def logout(self: Self):
        ...


async def get_logout_controller() -> LogoutController:
    return LogoutController()


logout_controller = Annotated[
    protocols.LogoutUserControllerProtocol,
    Depends(get_logout_controller),
]
