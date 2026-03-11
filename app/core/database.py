from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import Config

config = Config()

TORTOISE_MODELS = [
    "app.models.wise_word_model",
    "app.models.user",
    "app.models.token_blacklist",
    "app.models.diary",
    "aerich.models",
]

DATABASE_URL = (
    f"postgres://{config.POSTGRES_USER}:"
    f"{config.POSTGRES_PASSWORD}@"
    f"{config.POSTGRES_HOST}:"
    f"{config.POSTGRES_PORT}/"
    f"{config.POSTGRES_DB}"
)


TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": TORTOISE_MODELS,
            "default_connection": "default",
        }
    },
}


# DB 테이블 생성
def init_tortoise(app: FastAPI) -> None:
    Tortoise.init_models(TORTOISE_MODELS, "models")
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
    )
