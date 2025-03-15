from datetime import datetime
from typing import Literal

import pytest

from container import Container
from core.config import JwtType


class RequestMock:
    def __init__(self, token: str | None = None) -> None:
        self.headers = {}
        self.cookies = {}
        if token:
            self.cookies[JwtType.REFRESH.value] = token


class ResponseMock:
    def __init__(self) -> None:
        self.cookie_setted = False


    def set_cookie(
            self,
            key: str,
            value: str = "",
            max_age: int | None = None,
            expires: datetime | str | int | None = None,
            path: str | None = "/",
            domain: str | None = None,
            secure: bool = False,
            httponly: bool = False,
            samesite: Literal['lax', 'strict', 'none'] | None = "lax",
    ) -> None:
        self.key = key
        self.value = value
        self.max_age = max_age
        self.expires = expires
        self.path = path
        self.domain = domain
        self.secure = secure
        self.httponly = httponly
        self.samesate = samesite

        self.cookie_setted = True



@pytest.fixture(scope="function")
def response() -> ResponseMock:
    return ResponseMock()


@pytest.fixture(scope="session")
def container() -> Container:
    return Container()



