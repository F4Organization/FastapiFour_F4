from tortoise.models import Model
from tortoise import fields

class WiseWord(Model):
    id = fields.IntField(pk=True)
    author = fields.CharField(max_length=255)
    content = fields.TextField()