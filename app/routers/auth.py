from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordBearer

from app.dependencies.auth import get_current_active_user, get_current_user
from app.models.user import User
from app.schemas.auth import (
    MessageResponse,
    LogoutRequest,
    TokenResponse,
    TokenRefreshRequest,
    UserLoginRequest,
    UserResponse,
    UserSignUpRequest,
)
from app.services.auth_service import auth_service
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=True,
)


@router.post("/signup", status_code=201, response_model=UserResponse)
async def signup(payload: UserSignUpRequest):
    """이메일 기반 회원가입을 수행한다."""
    user = await auth_service.signup(payload)
    return UserResponse(
        id=user.id,
        email=user.email,
        nickname=user.nickname,
        created_at=user.created_at,
    )


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLoginRequest):
    """이메일/비밀번호로 로그인하고 JWT를 발급한다."""
    (
        access_token,
        expires_in,
        access_expires_at,
        refresh_token,
        refresh_expires_in,
        refresh_expires_at,
        _,
    ) = await auth_service.login(payload)
    return TokenResponse(
        access_token=access_token,
        access_expires_at=access_expires_at,
        refresh_token=refresh_token,
        refresh_expires_at=refresh_expires_at,
        expires_in=expires_in,
        refresh_expires_in=refresh_expires_in,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: TokenRefreshRequest):
    """리프레시 토큰으로 새 JWT 쌍을 발급한다."""
    (
        access_token,
        expires_in,
        access_expires_at,
        refresh_token,
        refresh_expires_in,
        refresh_expires_at,
        _,
    ) = await auth_service.refresh(payload.refresh_token)
    return TokenResponse(
        access_token=access_token,
        access_expires_at=access_expires_at,
        refresh_token=refresh_token,
        refresh_expires_at=refresh_expires_at,
        expires_in=expires_in,
        refresh_expires_in=refresh_expires_in,
    )


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_active_user)):
    """현재 로그인한 사용자의 정보를 조회한다."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        nickname=current_user.nickname,
        created_at=current_user.created_at,
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: User = Depends(get_current_user),
    token: str = Depends(_oauth2_scheme),
    payload: LogoutRequest | None = Body(default=None),
):
    """현재 토큰을 블랙리스트에 등록해 로그아웃 처리한다."""
    await auth_service.logout(
        access_token=token,
        user=current_user,
        refresh_token=payload.refresh_token if payload is not None else None,
    )
    return MessageResponse(message=f"{current_user.email} 로그아웃 처리 완료")
