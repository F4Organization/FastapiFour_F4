from app.core.config import settings

DATABASE_URL = (
    f"postgres://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}