from dataclasses import dataclass


@dataclass
class RefreshJwtDto:
    access_jwt: str


@dataclass
class UserLoginDto(RefreshJwtDto):
    """Data Transfer Object from user login usecase."""
    refresh_jwt: str


@dataclass
class UserRegisterDto(UserLoginDto):
    username: str


