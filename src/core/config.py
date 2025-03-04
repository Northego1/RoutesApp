from typing import Self

from pydantic_settings import BaseSettings, SettingsConfigDict


class CustomSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class DataBase(CustomSettings):
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_NAME: str = "postgres"
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


class Settings:
    def __init__(self: Self) -> None:
        self.db = DataBase()


settings = Settings()
