from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class UserSignUpRequest(BaseModel):
    """회원가입 요청 입력 스펙을 검증하는 Pydantic 모델."""

    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="Password")
    confirm_password: str = Field(..., description="Password confirmation")
    nickname: str | None = Field(default=None, max_length=20, description="Nickname")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """비밀번호 최소 길이를 검증한다."""
        normalized = value.strip()
        if len(normalized) < 8:
            raise ValueError("비밀번호는 최소 8자 이상이어야 합니다.")
        elif len(normalized) > 30:
            raise ValueError("비밀번호는 최대 30자 이하이어야 합니다.")
        return normalized
        
        
    @model_validator(mode="after")
    def validate_confirm_password(self) -> "UserSignUpRequest":
        """비밀번호 확인 항목이 일치하는지 검증한다."""
        if self.password != self.confirm_password:
            raise ValueError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        return self


class UserLoginRequest(BaseModel):
    """로그인 요청 입력 스펙을 검증하는 Pydantic 모델."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=30)


class UserResponse(BaseModel):
    """로그인된 사용자 기본 정보를 응답하기 위한 스키마."""

    id: int
    email: EmailStr
    nickname: str | None = None
    created_at: datetime


class TokenResponse(BaseModel):
    """토큰 발급 응답 스키마."""

    access_token: str
    access_expires_at: datetime
    refresh_expires_at: datetime
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_expires_in: int


class TokenRefreshRequest(BaseModel):
    """리프레시 토큰으로 새 토큰을 발급받기 위한 요청 스키마."""

    refresh_token: str


class APIErrorResponse(BaseModel):
    """표준 에러 응답 스키마."""

    ok: bool = False
    code: str
    message: str
    detail: object | None = None


class LogoutRequest(BaseModel):
    """로그아웃 시 함께 무효화할 리프레시 토큰 입력 스키마."""

    refresh_token: str | None = Field(
        default=None,
        description="선택: 로그아웃 대상 refresh token",
    )


class MessageResponse(BaseModel):
    """일반 메시지 응답 스키마."""

    message: str
