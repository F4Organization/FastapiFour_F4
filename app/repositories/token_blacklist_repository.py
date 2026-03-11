from datetime import datetime, timezone

from app.models.token_blacklist import TokenBlacklist
from app.models.user import User


class TokenBlacklistRepository:
    """블랙리스트에 기록된 토큰을 관리한다."""

    async def add(
        self,
        token: str,
        user: User,
        expires_at: datetime | None = None,
    ) -> TokenBlacklist:
        """토큰을 블랙리스트에 추가한다."""
        return await TokenBlacklist.create(
            token=token,
            user=user,
            expires_at=expires_at,
        )

    async def exists(self, token: str) -> bool:
        """토큰이 블랙리스트에 존재하는지 확인한다."""
        now = datetime.now(timezone.utc)
        await self.purge_expired()
        return await TokenBlacklist.filter(
            token=token,
            expires_at__gt=now,
        ).exists()

    async def purge_expired(self) -> int:
        """만료된 블랙리스트 토큰을 정리한다."""
        now = datetime.now(timezone.utc)
        return await TokenBlacklist.filter(expires_at__lte=now).delete()


token_blacklist_repository = TokenBlacklistRepository()
