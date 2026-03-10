<<<<<<< HEAD
from enum import StrEnum
=======
>>>>>>> 6047c55 ( ✨ feat(auth): implement refresh/logout/blacklist flow)
from pathlib import Path
from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic_settings import BaseSettings


class Env(StrEnum):
    LOCAL = "local"
    STAGE = "stage"
    PROD = "prod"


class Config(BaseSettings):
    """프로젝트 공통 설정."""

    ENV: Env = Env.LOCAL
    PROJECT_NAME: str = "FastAPI Four"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080
    DATABASE_URL: str | None = None

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"
    CONNECTION_POOL_MAXSIZE: int = 10
    GENERATE_SCHEMAS: bool = True

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def database_url(self) -> str:
        """PostgreSQL/SQLite용 DB URL를 반환한다."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgres://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Config()


__all__ = ["Env", "Config", "settings"]
