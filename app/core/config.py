from enum import StrEnum
from pydantic_settings import BaseSettings
from pathlib import Path

class Env(StrEnum):
    LOCAL = "local"
    STAGE = "stage"
    PROD = "prod"

class Config(BaseSettings):
    ENV: Env = Env.LOCAL

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    CONNECTION_POOL_MAXSIZE: int = 10

    class Config:
        env_path = Path(__file__).resolve().parent.parent.parent / ".env"  # .env 파일 지정
        env_file_encoding = "utf-8"