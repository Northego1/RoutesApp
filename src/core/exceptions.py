from typing import Self


class BaseError(Exception):
    def __init__(
            self: Self,
            detail: str | dict | list = "UknownError",
            status_code: int = 500,
            *args: object,
    ) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(*args)