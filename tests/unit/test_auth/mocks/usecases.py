from copy import copy
from typing import TYPE_CHECKING, cast
from unittest.mock import AsyncMock, Mock

from apps.auth.application.dto import RefreshJwtDto
from core.exceptions import BaseError
from tests.unit.test_auth.common import Mck

if TYPE_CHECKING:
    from apps.auth.application.usecases.login_usecase import LoginUsecase
    from apps.auth.application.usecases.refresh_jwt_usecase import RefreshJwtUsecase
    from apps.auth.application.usecases.register_usecase import RegisterUsecase


login_usecase_mock = cast("LoginUsecase", Mock())
register_usecase_mock = cast("RegisterUsecase", Mock())
refresh_usecase_mock = cast("RefreshJwtUsecase", Mock())


def login_effect(username: str, password: str):  # noqa: ANN201
    if password != Mck.req.login_request.password or \
    username != Mck.req.login_request.username:
        raise BaseError
    return copy(Mck.dto.login_dto)

def register_effect(username: str, password: str, email: str):  # noqa: ANN201
    if password != Mck.req.register_request.password or \
    username != Mck.req.register_request.username or \
    email != Mck.req.register_request.email:
        raise BaseError
    return copy(Mck.dto.register_dto)

def refresh_effect(refresh_jwt: str) -> RefreshJwtDto:
    if refresh_jwt != Mck.ent.refresh_token_domain.token:
        raise BaseError
    return copy(Mck.dto.refresh_dto)

login_usecase_mock.execute = AsyncMock(
    side_effect=login_effect,
)

register_usecase_mock.execute = AsyncMock(
    side_effect=register_effect,
)

refresh_usecase_mock.execute = AsyncMock(
    side_effect=refresh_effect,
)
