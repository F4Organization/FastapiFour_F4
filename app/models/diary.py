from tortoise import fields
from tortoise.models import Model
from datetime import datetime

class Diary(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()  # users FK, 나중에 ForeignKeyField로 연결 가능
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(default=datetime.utcnow)
    updated_at = fields.DatetimeField(default=datetime.utcnow)

    class Meta:
        table = "diaries"