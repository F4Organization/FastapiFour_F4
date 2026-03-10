from tortoise import fields
from tortoise.models import Model

from app.models.user import User


class TokenBlacklist(Model):
    """로그아웃된 토큰을 저장해 재사용을 차단하는 모델."""

    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=2048, unique=True, db_index=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="token_blacklists", on_delete=fields.CASCADE
    )
    expires_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        """token_blacklists 테이블 이름을 지정한다."""

        table = "token_blacklists"
