from tortoise import fields
from tortoise.models import Model


# 명언 수집 저장 테이블
class WiseWord(Model):
    id = fields.IntField(pk=True)
    author = fields.CharField(max_length=255, null=False)
    content = fields.TextField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)  # UTC로 저장
    wise_word_bookmark = fields.ReverseRelation["BookmarkedWiseWord"]

    class Meta:
        table = "wise_words"

# 유저의 북마크 저장용 테이블
class BookmarkedWiseWord(Model):
    id = fields.IntField(pk=True)
    user_id = fields.ForeignKeyField(
        model_name="models.User",
        related_name="user_bookmark",
        on_delete=fields.CASCADE,
        null=False,
    )
    wise_word_id = fields.ForeignKeyField(
        model_name="models.WiseWord",
        related_name="wise_word_bookmark",
        on_delete=fields.CASCADE,
        null=False,
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "bookmarked_wise_words"