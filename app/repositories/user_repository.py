from app.models.user_model import User


class UserRepository:
    """User 엔티티의 데이터베이스 접근을 담당하는 저장소."""

    async def get_by_email(self, email: str) -> User | None:
        """이메일로 사용자를 조회한다."""
        return await User.get_or_none(email=email)

    async def get_by_id(self, user_id: int) -> User | None:
        """PK로 사용자를 조회한다."""
        return await User.get_or_none(id=user_id)

    async def create(
        self,
        email: str,
        hashed_password: str,
        nickname: str | None = None,
    ) -> User:
        """새 사용자 계정을 생성하고 저장한다."""
        return await User.create(
            email=email,
            hashed_password=hashed_password,
            nickname=nickname,
        )


user_repository = UserRepository()
