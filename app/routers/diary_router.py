from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.diary_schema import DiaryCreate, DiaryUpdate, DiaryOut
from app.services.diary_service import create_diary, get_diary, update_diary, delete_diary, list_diaries
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/diaries", tags=["diaries"])

@router.post("/", response_model=DiaryOut)
async def create(diary_in: DiaryCreate, current_user=Depends(get_current_user)):
    return await create_diary(user_id=current_user.id, diary_in=diary_in)

@router.get("/", response_model=List[DiaryOut])
async def read_all(current_user=Depends(get_current_user)):
    return await list_diaries(user_id=current_user.id)

@router.get("/{diary_id}", response_model=DiaryOut)
async def read(diary_id: int, current_user=Depends(get_current_user)):
    diary = await get_diary(diary_id)
    if not diary or diary.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diary not found")
    return diary

@router.patch("/{diary_id}", response_model=DiaryOut)
async def update(diary_id: int, diary_in: DiaryUpdate, current_user=Depends(get_current_user)):
    diary = await get_diary(diary_id)
    if not diary or diary.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diary not found")
    return await update_diary(diary_id, diary_in)

@router.delete("/{diary_id}")
async def delete(diary_id: int, current_user=Depends(get_current_user)):
    diary = await get_diary(diary_id)
    if not diary or diary.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diary not found")
    await delete_diary(diary_id)
    return {"message": "Diary deleted"}