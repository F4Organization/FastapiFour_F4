# from fastapi import FastAPI, HTTPException, Request
# from fastapi.exceptions import RequestValidationError
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from app.core.config import Env, settings
# from app.core.database import init_tortoise
# from app.routers import auth_router
# from app.schemas.auth import APIErrorResponse
#
#
# def _build_error_payload(detail: object) -> APIErrorResponse:
#     """오류 상세를 공통 스키마로 정규화한다."""
#     if isinstance(detail, dict) and all(key in detail for key in ("code", "message")):
#         code = str(detail.get("code", "UNKNOWN_ERROR"))
#         message = str(detail.get("message", "알 수 없는 오류"))
#         normalized_detail = detail.get("detail")
#         return APIErrorResponse(code=code, message=message, detail=normalized_detail)
#     if isinstance(detail, str):
#         return APIErrorResponse(code="GENERIC_ERROR", message=detail, detail=None)
#
#     return APIErrorResponse(
#         code="REQUEST_VALIDATION_ERROR",
#         message="요청 파싱/검증에 실패했습니다.",
#         detail=detail,
#     )
#
#
# app = FastAPI(title=settings.PROJECT_NAME, debug=settings.ENV == Env.LOCAL)
# app.include_router(auth_router, prefix=settings.API_V1_STR)
# init_tortoise(app)
#
#
# @app.exception_handler(HTTPException)
# async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
#     payload = _build_error_payload(exc.detail)
#     return JSONResponse(
#         status_code=exc.status_code,
#         content=payload.model_dump(),
#         headers=getattr(exc, "headers", None),
#     )
#
#
# @app.exception_handler(RequestValidationError)
# async def request_validation_exception_handler(
#     _: Request, exc: RequestValidationError
# ) -> JSONResponse:
#     payload = APIErrorResponse(
#         code="REQUEST_VALIDATION_ERROR",
#         message="요청 검증에 실패했습니다.",
#         detail=jsonable_encoder(exc.errors()),
#     )
#     return JSONResponse(status_code=422, content=payload.model_dump())
#
#
# @app.exception_handler(Exception)
# async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
#     payload = APIErrorResponse(
#         code="INTERNAL_SERVER_ERROR",
#         message="예기치 못한 서버 오류가 발생했습니다.",
#         detail=str(exc),
#     )
#     return JSONResponse(status_code=500, content=payload.model_dump())

from fastapi import FastAPI

from app.core.database import init_tortoise

app = FastAPI()

# 데이터베이스 연결 초기화
init_tortoise(app)