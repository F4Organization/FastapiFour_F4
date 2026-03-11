from tortoise import fields
from tortoise.models import Model


# 명언 수집 데이터베이스
class WiseWord(Model):
    id = fields.IntField(pk=True)
    author = fields.CharField(max_length=255, null=False)
    content = fields.TextField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)  # UTC로 저장
