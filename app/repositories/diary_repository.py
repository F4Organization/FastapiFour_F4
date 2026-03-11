from app.models.diary import Diary


async def create_diary(title: str, content: str):
    return await Diary.create(title=title, content=content)


async def get_diaries(user_id: int):
    return await Diary.filter(user_id=user_id)


async def get_diary(diary_id: int):
    return await Diary.get_or_none(id=diary_id)


async def delete_diary(diary_id: int):
    diary = await Diary.get(id=diary_id)
    await diary.delete()