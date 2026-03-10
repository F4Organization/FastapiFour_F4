from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.core.database import TORTOISE_ORM

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "FastAPI + PostgreSQL connected"}