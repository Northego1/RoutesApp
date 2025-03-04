from typing import Annotated, Self

from fastapi import Depends

from api.v1 import protocols


class LoginController:
    def __init__(self: Self) -> None:
        pass


    async def login():
        ...


async def get_login_controller() -> LoginController:
    return LoginController()


login_controller = Annotated[
    protocols.LoginUserControllerProtocol,
    Depends(get_login_controller),
]
