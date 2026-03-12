from fastapi import APIRouter, status, Depends
from typing import List

from app.schemas.diary_schema import DiaryCreate, DiaryResponse
from app.services import diary_service
from app.dependencies.auth import get_current_user
from app.models.user_model import User

# /diaries 로 시작하는 API 그룹 생성
router = APIRouter(prefix="/diaries", tags=["Diary"])


@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
async def create_diary(
    data: DiaryCreate,
    current_user: User = Depends(get_current_user)
):
    """
    새로운 일기를 생성합니다.

    - JWT 토큰을 통해 현재 로그인한 사용자를 가져옵니다.
    - 클라이언트가 user_id를 보내지 않도록 하여 보안을 유지합니다.
    """

    # 현재 로그인한 사용자의 id를 이용해 일기 생성
    return await diary_service.create_diary(
        user_id=current_user.id,
        title=data.title,
        content=data.content
    )


@router.get("/", response_model=List[DiaryResponse])
async def read_diaries(
    current_user: User = Depends(get_current_user)
):
    """
    현재 로그인한 사용자의 모든 일기를 조회합니다.

    - user_id를 파라미터로 받지 않습니다.
    - JWT 토큰에서 추출한 사용자 id로 조회합니다.
    """

    return await diary_service.get_diaries(current_user.id)


@router.get("/{diary_id}", response_model=DiaryResponse)
async def read_diary(
    diary_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    특정 일기 하나를 조회합니다.

    - diary_id는 path parameter로 받습니다.
    - 인증된 사용자만 접근 가능합니다.
    """

    return await diary_service.get_diary(diary_id)


@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
    diary_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    특정 일기를 삭제합니다.

    - 인증된 사용자만 삭제할 수 있습니다.
    - 실제 서비스에서는 보통 작성자 검증 로직이 추가됩니다.
    """

    await diary_service.delete_diary(diary_id)