import contextlib
from typing import TYPE_CHECKING, cast
from unittest.mock import AsyncMock, Mock

from unit.test_auth.mocks.repositories import refresh_jwt_repository_mock, user_repository_mock

if TYPE_CHECKING:
    from core.uow import UnitOfWork


uow_mock = cast("UnitOfWork", Mock())


class RepositoryMock:
    user_repository = user_repository_mock
    refresh_repository = refresh_jwt_repository_mock


class Uow:
    async def __aenter__(self):
        return RepositoryMock()

    async def __aexit__(self, *args):
        pass



uow_mock.transaction = Mock(side_effect=Uow)
