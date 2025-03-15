from copy import copy

import pytest
from dependency_injector import providers

from apps.auth.application.usecases.refresh_jwt_usecase import RefreshJwtUsecase
from container import Container
from core.exceptions import BaseError
from core.schema import ApiResponse
from tests.unit.test_auth.common import Mck
from tests.unit.test_auth.mocks.security import security_mock
from tests.unit.test_auth.mocks.uow import uow_mock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("refresh_jwt", "expect", "exception"),
    [
        (
            Mck.ent.refresh_token_domain.token,
            Mck.dto.refresh_dto,
            None,
        ),
        (
            "notcorrect token",
            None,
            BaseError,
        ),
    ],
)
async def test_register_usecase(  # noqa: PLR0913
    container: Container,
    refresh_jwt: str,
    expect: ApiResponse | None,
    exception: type[BaseError] | None,
) -> None:
    container.usecases.refresh_jwt_usecase.override(
        providers.Factory(
            RefreshJwtUsecase,
            uow=uow_mock,
            security=security_mock,
        ),
    )
    refresh_usecase: RefreshJwtUsecase = container.usecases.refresh_jwt_usecase()


    if exception:
        with pytest.raises(exception):
            await refresh_usecase.execute(
            refresh_jwt=refresh_jwt,
        )
    else:
        resp = await refresh_usecase.execute(
            refresh_jwt=refresh_jwt,
        )
        assert resp == expect

