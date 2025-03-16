from copy import copy
from typing import TYPE_CHECKING, cast
from unittest.mock import AsyncMock, Mock

from apps.auth.application import dto
from core.exceptions import BaseError
from tests.unit.test_auth.common import Mck

if TYPE_CHECKING:
    from apps.auth.application.usecases.get_me_usecase import GetMeUsecase
    from apps.auth.application.usecases.login_usecase import LoginUsecase
    from apps.auth.application.usecases.logout_usecase import LogoutUsecase
    from apps.auth.application.usecases.refresh_jwt_usecase import RefreshJwtUsecase
    from apps.auth.application.usecases.register_usecase import RegisterUsecase

logout_usecase_mock = cast("LogoutUsecase", Mock())
login_usecase_mock = cast("LoginUsecase", Mock())
register_usecase_mock = cast("RegisterUsecase", Mock())
refresh_usecase_mock = cast("RefreshJwtUsecase", Mock())
getme_usecase_mock = cast("GetMeUsecase", Mock())


def login_effect(username: str, password: str) -> dto.UserLoginDto:
    if password != Mck.req.login_request.password or \
        username != Mck.req.login_request.username:
        raise BaseError
    return copy(Mck.dto.login_dto)

def register_effect(username: str, password: str, email: str) -> dto.UserRegisterDto:
    if password != Mck.req.register_request.password or \
        username != Mck.req.register_request.username or \
        email != Mck.req.register_request.email:
        raise BaseError
    return copy(Mck.dto.register_dto)

def refresh_effect(refresh_jwt: str) -> dto.RefreshJwtDto:
    if refresh_jwt != Mck.ent.refresh_token_domain.token:
        raise BaseError
    return copy(Mck.dto.refresh_dto)

def getme_effect(access_token: str) -> dto.UserDto:
    if access_token != Mck.ent.access_token_domain.token:
        raise BaseError
    return copy(Mck.dto.user_dto)

async def logout_effect(
        refresh_token: str | None,
        access_token: str | None,
) -> None:
    if not refresh_token and not access_token:
        raise BaseError(status_code=401)
    if refresh_token == Mck.ent.access_token_domain.token or \
        access_token == Mck.ent.refresh_token_domain.token:
        raise BaseError(status_code=401)



login_usecase_mock.execute = AsyncMock(
    side_effect=login_effect,
)

register_usecase_mock.execute = AsyncMock(
    side_effect=register_effect,
)

refresh_usecase_mock.execute = AsyncMock(
    side_effect=refresh_effect,
)

getme_usecase_mock.execute = AsyncMock(
    side_effect=getme_effect,
)

logout_usecase_mock.execute = AsyncMock(
    side_effect=logout_effect,
)
