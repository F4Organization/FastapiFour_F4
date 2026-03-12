from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt, JWTError  # type: ignore[import-not-found]
from passlib.context import CryptContext  # type: ignore[import-not-found]

from app.core.config import Config


config = Config()

# Use a backend-stable default hash for local/dev tests and CI.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class TokenError(Exception):
    """JWT 토큰 관련 예외를 표시하기 위한 사용자 정의 예외."""


def hash_password(password: str) -> str:
    """평문 비밀번호를 해시해서 반환"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """평문 비밀번호와 해시된 비밀번호가 일치하는지 검증한다."""
    return pwd_context.verify(plain_password, hashed_password)


def _build_token_payload(
    subject: str | int,
    email: str,
    token_type: str,
    expires_delta: timedelta | None,
) -> tuple[dict[str, Any], datetime, int]:
    """토큰 payload 생성과 만료 초 계산을 공통 처리한다."""
    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta
        or timedelta(
            minutes=(
                config.ACCESS_TOKEN_EXPIRE_MINUTES
                if token_type == "access"
                else config.REFRESH_TOKEN_EXPIRE_MINUTES
            )
        )
    )
    payload: dict[str, Any] = {
        "sub": str(subject),  # user_id
        "email": email,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    expire_in = int((expire - now).total_seconds())
    return payload, expire, expire_in


def _create_jwt_token(payload: dict[str, Any]) -> str:
    """JWT 문자열을 생성해 반환한다."""
    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)


def create_access_token(
    subject: str | int,
    email: str,
    expires_delta: timedelta | None = None,
) -> tuple[str, datetime, int]:
    """
    JWT 엑세스 토큰 생성
    반환값: (token, expiration_in_seconds)
    """
    payload, expires_at, expire_in = _build_token_payload(
        subject, email, "access", expires_delta
    )
    token = _create_jwt_token(payload)
    return token, expires_at, expire_in


def create_refresh_token(
    subject: str | int,
    email: str,
    expires_delta: timedelta | None = None,
) -> tuple[str, datetime, int]:
    """
    JWT 리프레시 토큰 생성
    반환값: (token, expiration_in_seconds)
    """
    payload, expires_at, expire_in = _build_token_payload(subject, email, "refresh", expires_delta)
    token = _create_jwt_token(payload)
    return token, expires_at, expire_in


def decode_token(token: str, expected_type: str | None = None) -> dict[str, Any]:
    """JWT 토큰 검증 및 payload 반환"""
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
    except JWTError as e:
        raise TokenError("유효하지 않거나 만료된 토큰입니다.") from e

    if expected_type and payload.get("type") != expected_type:
        raise TokenError(f"{expected_type} 토큰이 아닙니다.")

    if not payload.get("sub"):
        raise TokenError("토큰에 사용자 정보가 없습니다.")
    if payload.get("exp") is None:
        raise TokenError("토큰 만료시각이 없습니다.")

    return payload


def decode_access_token(token: str) -> dict[str, Any]:
    """JWT 엑세스 토큰 검증 및 payload 반환"""
    return decode_token(token, expected_type="access")


def decode_refresh_token(token: str) -> dict[str, Any]:
    """JWT 리프레시 토큰 검증 및 payload 반환"""
    return decode_token(token, expected_type="refresh")
