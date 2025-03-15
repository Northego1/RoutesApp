import pytest
from dependency_injector import providers
from fastapi import HTTPException

from apps.auth import presentation as present
from apps.auth.presentation.schemas.requests import RegisterRequest
from container import Container
from core.exceptions import BaseError
from core.schema import ApiResponse, Status
from tests.unit.test_auth.common import Mck
from tests.unit.test_auth.mocks import usecases as uc


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("register_request", "expect", "exception"),
    [
        (
            RegisterRequest(
                username=Mck.req.register_request.username,
                password=Mck.req.register_request.password,
                email=Mck.req.register_request.email,
            ),
            ApiResponse(
                status=Status.SUCCESS,
                data=Mck.resp.register_response,
            ),
            None,
        ),
        (
            RegisterRequest(
                username=Mck.req.register_request.username,
                password="wrong",  # noqa: S106
                email=Mck.req.register_request.email,
            ),
            None,
            HTTPException,
        ),
        (
            RegisterRequest(
                username="wrong",
                password=Mck.req.register_request.password,
                email=Mck.req.register_request.email,
            ),
            None,
            HTTPException,
        ),
    ],
)
async def test_register(
    register_request: RegisterRequest,
    expect: ApiResponse | None,
    exception: type[BaseError] | None,
    response,
    container: Container,
) -> None:
    container.presentation.register.override(
        providers.Factory(
            present.RegisterController,
            register_usecase=uc.register_usecase_mock,
        ),
    )
    register_controller: present.RegisterController = container.presentation.register()


    if exception:
        with pytest.raises(exception):
            await register_controller.register(
            response,
            register_request,
        )
    else:
        resp = await register_controller.register(
            response,
            register_request,
        )
        assert resp == expect
        assert response.cookie_setted == True

