from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
<<<<<<< HEAD

from app.core.config import Config
=======
>>>>>>> 6047c55 ( ✨ feat(auth): implement refresh/logout/blacklist flow)

from app.core.config import settings

TORTOISE_MODELS = [
    "app.models.user",
    "app.models.token_blacklist",
    "app.models.wise_word_model",
    "aerich.models",
]

DATABASE_URL = settings.database_url


TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": TORTOISE_MODELS,
            "default_connection": "default",
        }
    },
}

def init_tortoise(app: FastAPI) -> None:
    """Tortoise ORM을 앱 라이프사이클에 바인딩한다."""
    Tortoise.init_models(TORTOISE_MODELS, "models")
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=settings.GENERATE_SCHEMAS,
    )
