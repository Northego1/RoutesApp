from copy import copy
from typing import TYPE_CHECKING, cast
from unittest.mock import Mock

from core.config import JwtType
from tests.unit.test_auth.common import Mck

if TYPE_CHECKING:
    from apps.auth.domain.token import Token
    from apps.auth.domain.user import User
    from apps.auth.infrastructure.utils.security import Security

security_mock = cast("Security", Mock())


def check_password(
    correct_password: bytes, checkable_password: bytes) -> bool:
    return correct_password == checkable_password


def decode_and_verify_jwt(token: str) -> "Token | None":
    if token == Mck.ent.refresh_token_domain.token:
        return Mck.ent.refresh_token_domain
    if token == Mck.ent.access_token_domain.token:
        return Mck.ent.access_token_domain
    return None

def create_jwt(user: "User", jwt_type: JwtType) -> "Token":
    match jwt_type:
        case JwtType.REFRESH:
            return copy(Mck.ent.refresh_token_domain)
        case JwtType.ACCESS:
            return copy(Mck.ent.access_token_domain)

security_mock.create_jwt = Mock(side_effect=create_jwt)
security_mock.check_password = Mock(side_effect=check_password)
security_mock.hash_password = Mock(return_value=copy(Mck.ent.user_domain.password))
security_mock.decode_and_verify_jwt = Mock(side_effect=decode_and_verify_jwt)
