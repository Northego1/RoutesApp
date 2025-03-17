from enum import Enum
from pathlib import Path
from typing import Annotated, Self

from pydantic import conint
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class ApiAccessType(str, Enum):
    PUBLIC = "/public"
    PROTECTED = "/protected"


class JwtType(str, Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class CustomSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class JwtSettings(CustomSettings):
    ACCESS_JWT_EXPIRE: int = 10  # minutes
    REFRESH_JWT_EXPIRE: int = 43200 # minutes (30 days)

    ALGORITHM: str = "RS256"

    PRIVATE_KEY: str = (
        BASE_DIR / "jwt_certs" / "jwt-private.pem"
    ).read_text()

    PUBLIC_KEY: str = (
        BASE_DIR / "jwt_certs" / "jwt-public.pem"
    ).read_text()



class DataBaseSettings(CustomSettings):
    DB_USER: str = "postgres"
    DB_PASS: str = "0420"
    DB_NAME: str = "routes"
    DB_HOST : str = "localhost"
    DB_PORT: str = "5432"

    CONN_POOL: int = 8
    MAX_OVERFLOW: int = 2
    TIMEOUT: int = 30
    CONN_RECYCLE: int = 180


    @property
    def dsn(self: Self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class AuthBussinesSettings(CustomSettings):
    MIN_USERNAME_LENGTH: Annotated[int, conint(ge=4)] = 7

    MIN_PASSWORD_LENGTH: Annotated[int, conint(ge=4)] = 7
    REQUIRED_UPPER_SYM: bool = True
    REQIRED_LOWER_SYM: bool = True
    REQUIRED_SPEC_SYM: bool = True
    REQUIRED_DIGIT: bool = True

    USER_REFRESH_JWT_LIMIT: int = 5


class GateWay(CustomSettings):
    VALHALLA_HOST: str = "VALHALLA_HOST"
    VALHALLA_PORT: str = "VALHALLA_PORT"
    overpass_request_url: str = "http://overpass-api.de/api/interpreter"


    def nominatim_request_url(self: Self, address: str) -> str:
        return f"https://nominatim.openstreetmap.org/search?q={address}&format=json"


    @property
    def valhalla_request_url(self: Self) -> str:
        return (
            f"http://{self.VALHALLA_HOST}:{self.VALHALLA_PORT}/route"
        )

class Settings:
    def __init__(self: Self) -> None:
        self.db = DataBaseSettings()
        self.auth = AuthBussinesSettings()
        self.jwt = JwtSettings()
        self.gateway = GateWay()


settings = Settings()
