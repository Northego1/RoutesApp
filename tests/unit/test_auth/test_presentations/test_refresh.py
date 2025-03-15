import pytest
from dependency_injector import providers
from fastapi import HTTPException

from apps.auth import presentation as present
from apps.auth.presentation.schemas.responses import RefreshAccessJwtResponse
from container import Container
from core.exceptions import BaseError
from core.schema import ApiResponse, Status
from tests.conftest import RequestMock
from tests.unit.test_auth.common import Mck
from tests.unit.test_auth.mocks import usecases as uc


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("request_", "expect", "exception"),
    [
        (
            RequestMock(Mck.ent.refresh_token_domain.token),
            ApiResponse(
                status=Status.SUCCESS,
                data=RefreshAccessJwtResponse(
                    access_jwt=Mck.ent.access_token_domain.token,
                ),
            ),
            None,
        ),
        (
            RequestMock("invalid token"),
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
async def test_refresh(
    request_: RequestMock,
    expect: ApiResponse | None,
    exception: type[BaseError] | None,
    container: Container,
) -> None:
    container.presentation.refresh_jwt.override(
        providers.Factory(
            present.RefreshController,
            refresh_jwt_usecase=uc.refresh_usecase_mock,
        ),
    )
    refresh_controller: present.RefreshController = container.presentation.refresh_jwt()


    if exception:
        with pytest.raises(exception):
            await refresh_controller.refresh(
            request=request_, # type: ignore
        )
    else:
        resp = await refresh_controller.refresh(
            request=request_, # type: ignore
        )
        assert resp == expect

