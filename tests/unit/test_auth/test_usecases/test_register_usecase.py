from copy import copy

import pytest
from dependency_injector import providers

from apps.auth.application.usecases.register_usecase import RegisterUsecase
from container import Container
from core.exceptions import BaseError
from core.schema import ApiResponse
from tests.unit.test_auth.common import Mck
from tests.unit.test_auth.mocks.security import security_mock
from tests.unit.test_auth.mocks.uow import uow_mock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("username", "password", "email", "expect", "exception"),
    [
        (
            Mck.ent.user_domain.username,
            Mck.ent.user_domain.password.decode(),
            Mck.ent.user_domain.email,
            copy(Mck.dto.register_dto),
            None,
        ),
        (
            "invalid",
            Mck.ent.user_domain.password.decode(),
            Mck.ent.user_domain.email,
            None,
            BaseError,
        ),
    ],
)
async def test_register_usecase(  # noqa: PLR0913
    container: Container,
    username: str,
    password: str,
    email: str | None,
    expect: ApiResponse | None,
    exception: type[BaseError] | None,
) -> None:
    container.usecases.register_usecase.override(
        providers.Factory(
            RegisterUsecase,
            uow=uow_mock,
            security=security_mock,
        ),
    )
    register_usecase: RegisterUsecase = container.usecases.register_usecase()


    if exception:
        with pytest.raises(exception):
            await register_usecase.execute(
            username=username,
            password=password,
            email=email,
        )
    else:
        resp = await register_usecase.execute(
            username=username,
            password=password,
            email=email,
        )
        assert resp == expect

