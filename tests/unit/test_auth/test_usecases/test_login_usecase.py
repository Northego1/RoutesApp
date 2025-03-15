from copy import copy

import pytest
from dependency_injector import providers

from apps.auth.application.usecases.login_usecase import LoginUsecase
from container import Container
from core.exceptions import BaseError
from core.schema import ApiResponse
from tests.unit.test_auth.common import Mck
from tests.unit.test_auth.mocks.security import security_mock
from tests.unit.test_auth.mocks.uow import uow_mock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("username", "password", "expect", "exception"),
    [
        (
            Mck.ent.user_domain.username,
            Mck.ent.user_domain.password.decode(),
            copy(Mck.dto.login_dto),
            None,
        ),
        (
            "Vasya",
            Mck.ent.user_domain.password.decode(),
            None,
            BaseError,
        ),
        (
            Mck.ent.user_domain.username,
            "123",
            None,
            BaseError,
        ),
    ],
)
async def test_login_usecase(
    username: str,
    password: str,
    expect: ApiResponse | None,
    exception: type[BaseError] | None,
    container: Container,
) -> None:
    container.usecases.login_usecase.override(
        providers.Factory(
            LoginUsecase,
            uow=uow_mock,
            security=security_mock,
        ),
    )
    login_usecase: LoginUsecase = container.usecases.login_usecase()


    if exception:
        with pytest.raises(exception):
            await login_usecase.execute(
            username=username,
            password=password,
        )
    else:
        resp = await login_usecase.execute(
            username=username,
            password=password,
        )
        assert resp == expect

