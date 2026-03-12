from app.models.diary_model import Diary


async def create_diary(user_id: int, title: str, content: str):
    return await Diary.create(
        user_id=user_id,
        title=title,
        content=content
    )

async def get_diaries(user_id: int):
    return await Diary.filter(user_id=user_id)


async def get_diary(diary_id: int):
    return await Diary.get_or_none(id=diary_id)


async def delete_diary(diary_id: int):
    diary = await Diary.get_or_none(id=diary_id)
    if diary:
        await diary.delete()