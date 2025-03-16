import pytest
from dependency_injector import providers
from fastapi import HTTPException

from apps.auth import presentation as present
from apps.auth.presentation.schemas.requests import LoginRequest
from container import Container
from core.config import JwtType
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
            RequestMock(headers={"Authorization": f"Bearer {Mck.ent.access_token_domain.token}"}),
            ApiResponse(
                status=Status.SUCCESS,
                data=Mck.resp.getme_response,
            ),
            None,
        ),
        (
            RequestMock(),
            None,
            HTTPException,
        ),
        (
            RequestMock(headers={"Authorization": "H s ms msms  s"}),
            None,
            HTTPException,
        ),
        (
            RequestMock(headers={"Authorization": "W"}),
            None,
            HTTPException,
        ),
        (
            RequestMock(headers={"Authorization": f"Bearer {Mck.ent.refresh_token_domain.token}"}),
            None,
            HTTPException,
        ),
    ],
)
async def test_login(
    request_: RequestMock,
    expect: ApiResponse | None,
    exception: type[BaseError] | None,
    container: Container,
) -> None:
    container.presentation.get_me.override(
        providers.Factory(
            present.GetMeController,
            get_user_usecase=uc.getme_usecase_mock,
        ),
    )
    get_me: present.GetMeController = container.presentation.get_me()


    if exception:
        with pytest.raises(exception):
            await get_me.get_me(
            request=request_, # type: ignore
        )
    else:
        resp = await get_me.get_me(
            request=request_, # type: ignore
        )
        assert resp == expect

