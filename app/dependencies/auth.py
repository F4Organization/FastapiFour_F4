from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError  # type: ignore[import-not-found]
from app.core.config import settings
from app.core.security import decode_access_token, TokenError
from app.repositories.user_repository import user_repository
from app.repositories.token_blacklist_repository import token_blacklist_repository
from app.models.user_model import User

oauth2_scheme_required = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=True,
)
oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False,
)


async def get_current_user(
    token: str = Depends(oauth2_scheme_required),
) -> User:
    """
    Access Token을 검증하고 현재 로그인한 사용자를 반환한다.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "AUTH_TOKEN_REQUIRED",
                "message": "인증에 필요한 토큰이 없습니다.",
                "detail": None,
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "code": "AUTH_TOKEN_INVALID",
            "message": "인증에 실패했습니다.",
            "detail": None,
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        if await token_blacklist_repository.exists(token):
            raise credentials_exception

        payload = decode_access_token(token)
        user_id_str: str | None = payload.get("sub")
        user_id = int(user_id_str) if user_id_str is not None else None
        if user_id is None:
            raise credentials_exception

    except (JWTError, TokenError, ValueError):
        raise credentials_exception

    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """활성 상태 유저만 통과시키는 인증 의존성."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "AUTH_USER_INACTIVE",
                "message": "비활성화된 사용자입니다.",
                "detail": None,
            },
        )
    return current_user


async def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme_optional),
) -> Optional[User]:
    """토큰이 없으면 None, 있으면 인증 사용자 객체를 반환한다."""
    if not token:
        return None

    try:
        if await token_blacklist_repository.exists(token):
            return None

        payload = decode_access_token(token)
        user_id_raw: str | None = payload.get("sub")
        user_id: int | None = int(user_id_raw) if user_id_raw is not None else None
        if user_id is None:
            return None
        user = await user_repository.get_by_id(user_id)
        return user

    except (JWTError, TokenError, ValueError):
        return None
def verify_self(target_user_id: int, current_user: User) -> None:
    """본인 요청인 경우에만 통과한다."""
    if current_user.id != target_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "AUTH_SELF_REQUIRED",
                "message": "본인의 정보만 수정할 수 있습니다.",
                "detail": None,
            },
        )
