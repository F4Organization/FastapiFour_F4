from app.repositories import diary_repository
from app.models.diary_model import Diary
from fastapi import HTTPException, status


async def create_diary(user_id: int, title: str, content: str) -> Diary:
    return await diary_repository.create_diary(user_id, title, content)

async def get_diaries(user_id: int) -> list[Diary]:
    return await diary_repository.get_diaries(user_id)


async def get_diary(diary_id: int, user_id: int) -> Diary | None:
    return await diary_repository.get_diary(diary_id=diary_id, user_id=user_id)


async def delete_diary(diary_id: int, user_id: int) -> None:
    bool_ = await diary_repository.delete_diary(diary_id=diary_id, user_id=user_id)
    if not bool_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

async def update_diary(user_id: int, diary_id: int, title: str, content: str) -> Diary:
    return await diary_repository.repo_update_diary(
        user_id=user_id,
        diary_id=diary_id,
        title=title,
        content=content
    )