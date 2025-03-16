import pytest
from dependency_injector import providers

from apps.auth.application.usecases.logout_usecase import LogoutUsecase
from container import Container
from core.exceptions import BaseError
from core.schema import ApiResponse
from tests.unit.test_auth.common import Mck
from tests.unit.test_auth.mocks.security import security_mock
from tests.unit.test_auth.mocks.uow import uow_mock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("access_token", "refresh_token", "expect", "exception"),
    [
        (
            Mck.ent.access_token_domain.token,
            None,
            None,
            None,
        ),
        (
            None,
            Mck.ent.refresh_token_domain.token,
            None,
            None,
        ),
        (
            Mck.ent.refresh_token_domain.token,
            None,
            None,
            BaseError,
        ),
        (
            None,
            Mck.ent.access_token_domain.token,
            None,
            BaseError,
        ),
        (
            None,
            None,
            None,
            BaseError,
        ),
    ],
)
async def test_logout_usecase(
    access_token: str | None,
    refresh_token: str | None,
    expect: ApiResponse | None,
    exception: type[BaseError] | None,
    container: Container,
) -> None:
    container.usecases.logout_usecase.override(
        providers.Factory(
            LogoutUsecase,
            uow=uow_mock,
            security=security_mock,
        ),
    )
    logout_usecase: LogoutUsecase = container.usecases.logout_usecase()


    if exception:
        with pytest.raises(exception):
            await logout_usecase.execute(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    else:
        resp =await logout_usecase.execute(
            access_token=access_token,
            refresh_token=refresh_token,
        )
        assert resp == expect

