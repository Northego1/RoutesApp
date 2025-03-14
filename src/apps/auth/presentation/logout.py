from typing import Self

from apps.auth.presentation import protocols as proto


class LogoutController:
    def __init__(
            self: Self,
            logout_service: proto.LoginUsecaseProtocol,
    ) -> None:
        pass


    async def logout(self: Self):
        ...

