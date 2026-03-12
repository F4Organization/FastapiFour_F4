from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from app.schemas.diary_schema import DiaryCreate, DiaryResponse, DiaryUpdateRequest, GetDiaryRequest
from app.services import diary_service
from app.dependencies.auth import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/diaries", tags=["Diary"])


@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
async def create_diary(
    data: DiaryCreate,
    current_user: User = Depends(get_current_user()),
) -> DiaryResponse:
    """
    새로운 일기를 생성합니다.
    """
    diary = await diary_service.create_diary(
        user_id=current_user.id,
        title=data.title,
        content=data.content
    )

    return DiaryResponse(
        diary_id=diary.id,
        title=diary.title,
        content=diary.content
    )


@router.get("/", response_model=List[DiaryResponse])
async def read_diaries(current_user: User = Depends(get_current_user)) -> List[DiaryResponse]:
    """
    특정 사용자의 모든 일기를 조회합니다.
    """
    user_id = current_user.id
    diaries = await diary_service.get_diaries(user_id)
    return diaries


@router.get("/{diary_id}", response_model=DiaryResponse)
async def read_diary(
        diary_id: GetDiaryRequest,
        current_user: User = Depends(get_current_user),
) -> DiaryResponse | None:
    """
    특정 일기 하나를 조회합니다.
    """
    diary = await diary_service.get_diary(diary_id=diary_id.diary_id, user_id=current_user.id)
    return DiaryResponse(diary_id=diary.id, title=diary.title, content=diary.content)


@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
        diary_id: GetDiaryRequest,
        current_user: User = Depends(get_current_user),
) -> dict:
    """
    특정 일기를 삭제합니다.
    """

    await diary_service.delete_diary(diary_id=diary_id.diary_id, user_id=current_user.id)
    return {"message": "Diary deleted successfully"}


@router.put("/{diary_id}", response_model=DiaryResponse)
async def api_update_diary(
        data: DiaryUpdateRequest,
        current_user: User = Depends(get_current_user),
) -> DiaryResponse:

    updated_diary = await diary_service.update_diary(
        user_id=current_user.id,
        diary_id=data.diary_id,
        title=data.title,
        content=data.content
    )

    return DiaryResponse(
        diary_id=updated_diary.id,
        title=updated_diary.title,
        content=updated_diary.content
    )

