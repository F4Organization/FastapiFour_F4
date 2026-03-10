from datetime import datetime, timezone

from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.token_blacklist_repository import token_blacklist_repository
from app.repositories.user_repository import user_repository
from app.schemas.auth import UserLoginRequest, UserSignUpRequest


def _to_datetime_if_present(timestamp: int | None) -> datetime | None:
    """UNIX timestamp를 UTC datetime으로 변환한다."""
    if timestamp is None:
        return None
    return datetime.fromtimestamp(int(timestamp), tz=timezone.utc)


def _auth_error(
    status_code: int, code: str, message: str, detail: object | None = None
):
    """에러 응답의 공통 규격을 보장하는 HTTPException 헬퍼."""
    raise HTTPException(
        status_code=status_code,
        detail={"code": code, "message": message, "detail": detail},
    )


class AuthService:
    """인증 관련 비즈니스 로직을 처리하는 서비스 레이어."""

    async def signup(self, payload: UserSignUpRequest):
        """이메일 중복 검사 후 사용자 등록을 수행한다."""
        existing = await user_repository.get_by_email(payload.email)
        if existing is not None:
            _auth_error(
                status.HTTP_409_CONFLICT,
                "AUTH_EMAIL_DUPLICATED",
                "이미 등록된 이메일입니다.",
            )

        hashed_password = hash_password(payload.password)
        user = await user_repository.create(
            email=payload.email,
            hashed_password=hashed_password,
            nickname=payload.nickname,
        )
        return user

    async def login(self, payload: UserLoginRequest):
        """이메일/비밀번호를 검증 후 JWT 토큰을 발급한다."""
        user = await user_repository.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.hashed_password):
            _auth_error(
                status.HTTP_401_UNAUTHORIZED,
                "AUTH_INVALID_CREDENTIALS",
                "이메일 또는 비밀번호가 올바르지 않습니다.",
            )

        if not user.is_active:
            _auth_error(
                status.HTTP_403_FORBIDDEN,
                "AUTH_USER_INACTIVE",
                "비활성화된 사용자입니다.",
            )

        access_token, expire_in = create_access_token(
            subject=user.id,
            email=user.email,
        )
        refresh_token, refresh_expire_in = create_refresh_token(
            subject=user.id,
            email=user.email,
        )
        return access_token, expire_in, refresh_token, refresh_expire_in, user

    async def refresh(self, refresh_token: str):
        """리프레시 토큰을 검증해 새 access/refresh 토큰을 발급한다."""
        if await token_blacklist_repository.exists(refresh_token):
            _auth_error(
                status.HTTP_401_UNAUTHORIZED,
                "AUTH_REFRESH_BLACKLIST",
                "무효화되거나 재사용된 refresh token입니다.",
            )

        payload = decode_refresh_token(refresh_token)
        user_id_raw = payload.get("sub")
        if user_id_raw is None:
            _auth_error(
                status.HTTP_401_UNAUTHORIZED,
                "AUTH_TOKEN_NO_SUB",
                "유효하지 않은 사용자 정보입니다.",
            )
        user_id = int(user_id_raw)

        user = await user_repository.get_by_id(user_id)
        if user is None:
            _auth_error(
                status.HTTP_401_UNAUTHORIZED,
                "AUTH_USER_NOT_FOUND",
                "사용자를 찾을 수 없습니다.",
            )
        if not user.is_active:
            _auth_error(
                status.HTTP_403_FORBIDDEN,
                "AUTH_USER_INACTIVE",
                "비활성화된 사용자입니다.",
            )

        expire_ts = payload.get("exp")
        expires_at = _to_datetime_if_present(expire_ts)
        try:
            await token_blacklist_repository.add(
                token=refresh_token,
                user=user,
                expires_at=expires_at,
            )
        except IntegrityError:
            pass

        access_token, expire_in = create_access_token(subject=user.id, email=user.email)
        new_refresh_token, refresh_expire_in = create_refresh_token(
            subject=user.id,
            email=user.email,
        )
        return access_token, expire_in, new_refresh_token, refresh_expire_in, user

    async def logout(
        self, access_token: str, user: User, refresh_token: str | None = None
    ):
        """현재 access/refresh 토큰을 블랙리스트에 저장해 로그아웃 처리한다."""
        await self._blacklist_access_token(access_token=access_token, user=user)

        if refresh_token is not None:
            await self._blacklist_refresh_token(refresh_token=refresh_token, user=user)

    async def _blacklist_access_token(self, access_token: str, user: User) -> None:
        """액세스 토큰 단건 블랙리스트에 추가한다."""
        payload = decode_access_token(access_token)
        user_id_raw = payload.get("sub")
        if user_id_raw is None:
            _auth_error(
                status.HTTP_401_UNAUTHORIZED,
                "AUTH_TOKEN_NO_SUB",
                "유효하지 않은 토큰입니다.",
            )

        if int(user_id_raw) != user.id:
            _auth_error(
                status.HTTP_403_FORBIDDEN,
                "AUTH_TOKEN_USER_MISMATCH",
                "현재 사용자와 토큰 주체가 일치하지 않습니다.",
            )

        expires_at = _to_datetime_if_present(payload.get("exp"))
        try:
            await token_blacklist_repository.add(
                token=access_token,
                user=user,
                expires_at=expires_at,
            )
        except IntegrityError:
            # 이미 블랙리스트에 들어간 토큰은 다시 추가하지 않는다.
            return

    async def _blacklist_refresh_token(self, refresh_token: str, user: User) -> None:
        """리프레시 토큰 단건 블랙리스트에 추가한다."""
        payload = decode_refresh_token(refresh_token)
        user_id_raw = payload.get("sub")
        if user_id_raw is None:
            _auth_error(
                status.HTTP_401_UNAUTHORIZED,
                "AUTH_TOKEN_NO_SUB",
                "유효하지 않은 refresh token입니다.",
            )

        if int(user_id_raw) != user.id:
            _auth_error(
                status.HTTP_403_FORBIDDEN,
                "AUTH_TOKEN_USER_MISMATCH",
                "현재 사용자와 refresh token 주체가 일치하지 않습니다.",
            )

        expires_at = _to_datetime_if_present(payload.get("exp"))
        try:
            await token_blacklist_repository.add(
                token=refresh_token,
                user=user,
                expires_at=expires_at,
            )
        except IntegrityError:
            # 이미 블랙리스트에 들어간 토큰은 다시 추가되지 않도록 idempotent 처리
            return


auth_service = AuthService()
