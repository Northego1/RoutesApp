from copy import copy
from typing import TYPE_CHECKING, cast
from unittest.mock import AsyncMock, Mock

from tests.unit.test_auth import common as cm

if TYPE_CHECKING:
    from apps.auth.infrastructure.repositories.refresh_jwt_repository import RefreshJwtRepository
    from apps.auth.infrastructure.repositories.user_repository import UserRepository


user_repository_mock = cast("UserRepository", Mock())
refresh_jwt_repository_mock = cast("RefreshJwtRepository", Mock())


user_repository_mock.get_user_by_id = AsyncMock(return_value=copy(cm.user_domain))
user_repository_mock.get_user_by_username = AsyncMock(return_value=copy(cm.user_domain))
user_repository_mock.create_user = AsyncMock(return_value=copy(cm.user_domain).id)
user_repository_mock.get_user_with_tokens = AsyncMock(return_value=copy(cm.user_domain))


refresh_jwt_repository_mock.update = AsyncMock(return_value=copy(cm.refresh_jwt_domain.id))
refresh_jwt_repository_mock.insert = AsyncMock(return_value=copy(cm.refresh_jwt_domain.id))
