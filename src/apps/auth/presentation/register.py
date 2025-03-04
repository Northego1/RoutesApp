from typing import Annotated, Self

from fastapi import Depends

from api.v1 import protocols


class RegisterController:
    def __init__(self: Self) -> None:
        pass

    def register(self: Self):
        ...



async def get_register_controller() -> RegisterController:
    return RegisterController()


register_controller = Annotated[
    protocols.RegisterUserControllerProtocol,
    Depends(get_register_controller)
]