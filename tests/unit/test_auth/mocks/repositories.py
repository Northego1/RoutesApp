import uuid
from copy import copy
from typing import TYPE_CHECKING, cast
from unittest.mock import AsyncMock, Mock

from tests.unit.test_auth .common import Mck

if TYPE_CHECKING:
    from apps.auth.domain.user import User
    from apps.auth.infrastructure.repositories.refresh_jwt_repository import RefreshJwtRepository
    from apps.auth.infrastructure.repositories.user_repository import UserRepository

user_repository_mock = cast("UserRepository", Mock())
refresh_jwt_repository_mock = cast("RefreshJwtRepository", Mock())


def get_user_effect_username(username: str, with_tokens: bool = False) -> "User | None":
    if username != Mck.ent.user_domain.username:
        return None
    if with_tokens:
        user = copy(Mck.ent.user_domain)
        user.token_list = []

    return copy(Mck.ent.user_domain)

def get_user_effect_user_id(user_id: uuid.UUID, with_tokens: bool = False) -> "User | None":
    if user_id != Mck.ent.user_domain.id:
        return None
    if with_tokens:
        user = copy(Mck.ent.user_domain)
        user.token_list = []

    return copy(Mck.ent.user_domain)


def create_user_effect(user: "User") -> uuid.UUID | None:
    if user.username != Mck.ent.user_domain.username:
        return None
    return user.id

user_repository_mock.get_user_by_id = AsyncMock(side_effect=get_user_effect_user_id)
user_repository_mock.get_user_by_username = AsyncMock(side_effect=get_user_effect_username)
user_repository_mock.create_user = AsyncMock(side_effect=create_user_effect)


refresh_jwt_repository_mock.update = AsyncMock(
    return_value=copy(Mck.ent.refresh_token_domain.id))
refresh_jwt_repository_mock.insert = AsyncMock(
    return_value=copy(Mck.ent.refresh_token_domain.id))
