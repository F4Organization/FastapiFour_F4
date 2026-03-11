from app.models.diary import Diary
from typing import List
from app.schemas.diary_schema import DiaryCreate, DiaryUpdate

async def create_diary(user_id: int, diary_in: DiaryCreate) -> Diary:
    return await Diary.create(user_id=user_id, **diary_in.dict())

async def get_diary(diary_id: int) -> Diary | None:
    return await Diary.get_or_none(id=diary_id)

async def update_diary(diary_id: int, diary_in: DiaryUpdate) -> Diary | None:
    diary = await get_diary(diary_id)
    if diary:
        diary.update_from_dict(diary_in.dict(exclude_unset=True))
        await diary.save()
    return diary

async def delete_diary(diary_id: int) -> bool:
    diary = await get_diary(diary_id)
    if diary:
        await diary.delete()
        return True
    return False

async def list_diaries(user_id: int) -> List[Diary]:
    return await Diary.filter(user_id=user_id).all()