from fastapi import FastAPI

from app.core.database import init_tortoise

app = FastAPI()

# 데이터베이스 연결 초기화
init_tortoise(app)
