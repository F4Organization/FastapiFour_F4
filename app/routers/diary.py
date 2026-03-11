from fastapi import APIRouter
from app.schemas.diary import DiaryCreate
from app.services import diary_service

router = APIRouter(prefix="/diaries", tags=["Diary"])


@router.post("/")
async def create_diary(data: DiaryCreate):
    return await diary_service.create_diary(
        title=data.title,
        content=data.content
    )


@router.get("/")
async def read_diaries():
    return await diary_service.get_diaries()


@router.get("/{diary_id}")
async def read_diary(diary_id: int):
    return await diary_service.get_diary(diary_id)


@router.delete("/{diary_id}")
async def delete_diary(diary_id: int):
    return await diary_service.delete_diary(diary_id)