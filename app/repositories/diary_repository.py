from app.models.diary_model import Diary



async def create_diary(user_id: int, title: str, content: str) -> Diary:
    return await Diary.create(
        user_id=user_id,
        title=title,
        content=content
    )

async def get_diaries(user_id: int) -> list[Diary]:
    return await Diary.filter(user_id=user_id)


async def get_diary(diary_id: int, user_id: int) -> Diary | None:
    return await Diary.get_or_none(id=diary_id, user_id=user_id)


async def delete_diary(diary_id: int, user_id: int) -> bool:
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if diary:
        await diary.delete()
        return True
    else:
        return False

async def repo_update_diary(user_id: int, diary_id: int, title: str, content: str) -> Diary | None:
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if diary:
        diary.title = title
        diary.content = content
        await diary.save()
        return diary
    else:
        return None