from pathlib import Path
from enum import StrEnum

from pydantic_settings import BaseSettings


class Env(StrEnum):
    LOCAL = "local"
    STAGE = "stage"
    PROD = "prod"


class Config(BaseSettings):
    """프로젝트 공통 설정."""

    ENV: Env = Env.LOCAL
    PROJECT_NAME: str 
    API_V1_STR: str 
    SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080


    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str | int
    POSTGRES_DB: str
    CONNECTION_POOL_MAXSIZE: int = 10
    
    class Config:
        env_file = (
            Path(__file__).resolve().parent.parent.parent / ".env"
        )  # .env 파일 지정
        env_file_encoding = "utf-8"

