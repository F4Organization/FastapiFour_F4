from tortoise import fields
from tortoise.models import Model


class RandomQuestion(Model):
    id = fields.IntField(pk=True)
    question = fields.TextField()