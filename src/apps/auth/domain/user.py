from typing import Self
import uuid


class User:
    __slots__ = ()

    def __init__(
            self: Self,
            id: uuid.UUID,
            name: str,
            email: str
    ) -> None:
        pass