from fastapi import APIRouter, status
from typing import List

from app.schemas.diary_schema import DiaryCreate, DiaryResponse
from app.services import diary_service

router = APIRouter(prefix="/diaries", tags=["Diary"])


@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
async def create_diary(user_id: int, data: DiaryCreate):
    """
    새로운 일기를 생성합니다.
    """
    return await diary_service.create_diary(
        user_id=user_id,
        title=data.title,
        content=data.content
    )


@router.get("/", response_model=List[DiaryResponse])
async def read_diaries(user_id: int):
    """
    특정 사용자의 모든 일기를 조회합니다.
    """
    return await diary_service.get_diaries(user_id)


@router.get("/{diary_id}", response_model=DiaryResponse)
async def read_diary(diary_id: int):
    """
    특정 일기 하나를 조회합니다.
    """
    return await diary_service.get_diary(diary_id)


@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(diary_id: int):
    """
    특정 일기를 삭제합니다.
    """
    await diary_service.delete_diary(diary_id)