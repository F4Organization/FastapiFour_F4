from tortoise import fields
from tortoise.models import Model


class User(Model):
    """사용자 인증 정보를 저장하는 Tortoise ORM 모델."""

    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True, index=True)
    hashed_password = fields.CharField(max_length=255, null=False)
    nickname = fields.CharField(max_length=20, null=False)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    user_bookmark = fields.ReverseRelation["BookmarkedWiseWord"]
    diaries = fields.ReverseRelation["Diary"]

    class Meta:
        """users 테이블 이름을 지정한다."""

        table = "users"
