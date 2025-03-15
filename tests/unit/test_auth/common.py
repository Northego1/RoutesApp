import uuid
from datetime import UTC, datetime, timedelta

from apps.auth.application import dto
from apps.auth.domain.token import Token
from apps.auth.domain.user import User
from apps.auth.presentation.schemas import requests, responses
from core.config import settings

TEST_USER_UUID = uuid.UUID("41e56f2b-f355-41f7-b281-8b2cd4ca5454")
TEST_USERNAME = "TestUserName"
TEST_PASSWORD = "TestPassword1!"
TEST_EMAIL = "user@user.com"

TEST_REFRESH_JWT_UUID = uuid.UUID("41e56f2f-f355-41f7-b281-8b2cd4ca5454")
TEST_REFRESH_JWT = "refresh_token"
TEST_REFRESH_EXPIRE = datetime.now(UTC) + timedelta(
    minutes=settings.jwt.REFRESH_JWT_EXPIRE,
)

TEST_ACCESS_JWT_UUID = uuid.UUID("42e56f2f-f355-41f7-b281-8b2cd4ca5454")
TEST_ACCESS_JWT = "access_token"
TEST_ACCESS_EXPIRE = datetime.now(UTC) + timedelta(
    minutes=settings.jwt.ACCESS_JWT_EXPIRE,
)


class _Entites:
    user_domain = User(
        id=TEST_USER_UUID,
        username=TEST_USERNAME,
        email=TEST_EMAIL,
        password=TEST_PASSWORD.encode(),
        token_list=[],
    )

    refresh_token_domain = Token(
        id=TEST_REFRESH_JWT_UUID,
        user_id=TEST_USER_UUID,
        token=TEST_REFRESH_JWT,  # noqa: S106
        token_expire=TEST_REFRESH_EXPIRE,
    )


    access_token_domain = Token(
        id=TEST_ACCESS_JWT_UUID,
        user_id=TEST_USER_UUID,
        token=TEST_ACCESS_JWT,  # noqa: S106
        token_expire=TEST_ACCESS_EXPIRE,
    )


class _Requests:
    register_request = requests.RegisterRequest(
        username=TEST_USERNAME,
        password=TEST_PASSWORD,  # noqa: S106
        email=TEST_EMAIL,
    )

    login_request = requests.LoginRequest(
        username=TEST_USERNAME,
        password=TEST_PASSWORD,  # noqa: S106
    )


class _Responses:
    login_response = responses.LoginResponse(access_jwt=TEST_ACCESS_JWT)

    register_response = responses.RegisterResponse(
        username=TEST_USERNAME, access_jwt=TEST_ACCESS_JWT)


class _Dto:
    login_dto = dto.UserLoginDto(
        access_jwt=TEST_ACCESS_JWT,
        refresh_jwt=TEST_REFRESH_JWT,
    )

    register_dto = dto.UserRegisterDto(
        username=TEST_USERNAME,
        access_jwt=TEST_ACCESS_JWT,
        refresh_jwt=TEST_REFRESH_JWT,
    )
    refresh_dto = dto.RefreshJwtDto(
        access_jwt=TEST_ACCESS_JWT,
    )



class Mck:
    dto = _Dto
    resp = _Responses
    ent = _Entites
    req = _Requests
