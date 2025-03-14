from copy import copy
from typing import TYPE_CHECKING, cast
from unittest.mock import AsyncMock, Mock

from core.exceptions import BaseError
from tests.unit.test_auth import common as cm

if TYPE_CHECKING:
    from apps.auth.application.usecases.login_usecase import LoginUsecase
    from apps.auth.application.usecases.register_usecase import RegisterUsecase


login_usecase_mock = cast("LoginUsecase", Mock())
register_usecase_mock = cast("RegisterUsecase", Mock())


def login_effect(username: str, password: str):  # noqa: ANN201
    if password != cm.login_request.password or \
    username != cm.login_request.username:
        raise BaseError
    return copy(cm.login_dto)

def register_effect(username: str, password: str, email: str):  # noqa: ANN201
    if password != cm.register_request.password or \
    username != cm.register_request.username or \
    email != cm.register_request.email:
        raise BaseError
    return copy(cm.register_dto)


login_usecase_mock.execute = AsyncMock(
    side_effect=login_effect,
)

register_usecase_mock.execute = AsyncMock(
    side_effect=register_effect,
)
