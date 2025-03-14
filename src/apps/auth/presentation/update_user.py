from typing import Self

from apps.auth.presentation import protocols as proto


class UpdateUserController:
    def __init__(
            self: Self,
            update_usecase: proto.UpdateUsecaseProtocol,
    ) -> None:
        self.update_uc = update_usecase


    async def update_user(self: Self):
        ...


