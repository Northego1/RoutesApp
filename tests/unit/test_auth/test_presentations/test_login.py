import pytest
from dependency_injector import providers
from fastapi import HTTPException

from apps.auth import presentation as present
from apps.auth.presentation.schemas.requests import LoginRequest
from container import Container
from core.exceptions import BaseError
from core.schema import ApiResponse, Status
from tests.unit.test_auth.common import Mck
from tests.unit.test_auth.mocks import usecases as uc


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("login_request", "expect", "exception"),
    [
        (
            LoginRequest(
                username=Mck.req.login_request.username,
                password=Mck.req.login_request.password,
            ),
            ApiResponse(
                status=Status.SUCCESS,
                data=Mck.resp.login_response,
            ),
            None,
        ),
        (
            LoginRequest(
                username=Mck.req.login_request.username,
                password="wrong",  # noqa: S106
            ),
            None,
            HTTPException,
        ),
        (
            LoginRequest(
                username="wrong",
                password=Mck.req.login_request.password,
            ),
            None,
            HTTPException,
        ),
    ],
)
async def test_login(
    login_request: LoginRequest,
    expect: ApiResponse | None,
    exception: type[BaseError] | None,
    response,
    container: Container,
) -> None:
    container.presentation.login.override(
        providers.Factory(
            present.LoginController,
            login_usecase=uc.login_usecase_mock,
        ),
    )
    login_controller: present.LoginController = container.presentation.login()


    if exception:
        with pytest.raises(exception):
            await login_controller.login(
            response,
            login_request,
        )
    else:
        resp = await login_controller.login(
            response,
            login_request,
        )
        assert resp == expect
        assert response.cookie_setted == True

