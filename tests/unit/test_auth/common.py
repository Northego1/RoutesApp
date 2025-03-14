import uuid
from datetime import UTC, datetime

from apps.auth.application import dto
from apps.auth.domain.refresh_jwt import RefreshJwt
from apps.auth.domain.user import User
from apps.auth.presentation.schemas import requests, responses

login_response = responses.LoginResponse(access_jwt="access_token")

register_response = responses.RegisterResponse(
    username="TestUserName", access_jwt="access_token")


register_request = requests.RegisterRequest(
    username="TestUserName",
    password="TestPassword1!",  # noqa: S106
    email="user@user.com",
)


login_request = requests.LoginRequest(
    username="TestUserName",
    password="TestPassword1",  # noqa: S106
)



login_dto = dto.UserLoginDto(
    access_jwt="access_token",
    refresh_jwt="refresh_jwt",
)

register_dto = dto.UserRegisterDto(
    username="TestUserName",
    access_jwt="access_token",
    refresh_jwt="refresh_jwt",
)



user_domain = User(
    id=uuid.UUID("41e56f2b-f355-41f7-b281-8b2cd4ca5454"),
    username="TestUserName",
    email="user@user.com",
    password=b"TestPassword1",
)

refresh_jwt_domain = RefreshJwt(
    id=uuid.UUID("41e56f2f-f355-41f7-b281-8b2cd4ca5454"),
    user_id=uuid.UUID("41e56f2b-f355-41f7-b281-8b2cd4ca5454"),
    token="refresh_jwt",  # noqa: S106
    token_expire=datetime.now(UTC),
)
