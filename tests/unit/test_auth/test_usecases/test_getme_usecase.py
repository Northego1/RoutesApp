from copy import copy

import pytest
from dependency_injector import providers

from apps.auth.application.usecases.get_me_usecase import GetMeUsecase
from container import Container
from core.exceptions import BaseError
from core.schema import ApiResponse
from tests.unit.test_auth.common import Mck
from tests.unit.test_auth.mocks.security import security_mock
from tests.unit.test_auth.mocks.uow import uow_mock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("access_jwt", "expect", "exception"),
    [
        (
            Mck.ent.access_token_domain.token,
            Mck.dto.user_dto,
            None,
        ),
        (
            "invalid",
            None,
            BaseError,
        ),
        (
            Mck.ent.refresh_token_domain.token,
            None,
            BaseError,
        ),
    ],
)
async def test_login_usecase(
    access_jwt: str,
    expect: ApiResponse | None,
    exception: type[BaseError] | None,
    container: Container,
) -> None:
    container.usecases.get_me_usecase.override(
        providers.Factory(
            GetMeUsecase,
            uow=uow_mock,
            security=security_mock,
        ),
    )
    login_usecase: GetMeUsecase = container.usecases.get_me_usecase()


    if exception:
        with pytest.raises(exception):
            await login_usecase.execute(
            access_token=access_jwt,
        )
    else:
        resp = await login_usecase.execute(
            access_token=access_jwt,
        )
        assert resp == expect

