from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas.random_question_schema import (
    RandomQuestionResponse,
    RandomQuestionCreate
)
from app.services.random_question_service import RandomQuestionService

router = APIRouter(prefix="/questions", tags=["questions"])
service = RandomQuestionService()


@router.get("/random", response_model=RandomQuestionResponse)
async def get_random_question():
    try:
        return await service.get_random_question()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("", response_model=RandomQuestionResponse)
async def create_random_question(request:RandomQuestionCreate):
    return await service.create_question(request.question)

@router.get("",response_model=List[RandomQuestionResponse])
async def get_all_questions():
    try:
        return await service.get_all_questions()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))