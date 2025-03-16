import pytest
from dependency_injector import providers
from fastapi import HTTPException

from apps.auth import presentation as present
from container import Container
from core.config import JwtType
from core.exceptions import BaseError
from core.schema import ApiResponse
from tests.conftest import RequestMock
from tests.unit.test_auth.common import Mck
from tests.unit.test_auth.mocks import usecases as uc


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("request_", "expect", "exception"),
    [
        (
            RequestMock(
            headers={"Authorization": f"Bearer {Mck.ent.access_token_domain.token}"},
            ),
            None,
            None,
        ),
        (
            RequestMock(
            cookies={JwtType.REFRESH.value: Mck.ent.refresh_token_domain.token},
            ),
            None,
            None,
        ),
        (
            RequestMock(
            headers={"Authorization": f"Bearer {Mck.ent.refresh_token_domain.token}"},
            ),
            None,
            HTTPException,
        ),
        (
            RequestMock(
            cookies={JwtType.REFRESH.value: Mck.ent.access_token_domain.token},
            ),
            None,
            HTTPException,
        ),
        (
            RequestMock(),
            None,
            HTTPException,
        ),
    ],
)
async def test_logout(
    request_: RequestMock,
    expect: ApiResponse | None,
    exception: type[BaseError] | None,
    container: Container,
) -> None:
    container.presentation.logout.override(
        providers.Factory(
            present.LogoutController,
            logout_usecase=uc.logout_usecase_mock,
        ),
    )
    logout_controller: present.LogoutController = container.presentation.logout()


    if exception:
        with pytest.raises(exception):
            await logout_controller.logout(
            request=request_, # type: ignore
        )
    else:
        resp = await logout_controller.logout(
            request=request_, # type: ignore
        )
        assert resp == expect

