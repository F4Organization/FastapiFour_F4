from fastapi import APIRouter, Depends, HTTPException

from app.models.user import User
from app.models.wise_word_model import WiseWord
from app.schemas.wise_word_schema import WiseWordResponse, BookMarkWiseWordRequest
from app.services.wise_words_service import get_random_wise_word, add_bookmark
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/wise_words", tags=["WiseWords"])

@router.get("/")
async def api_get_random_wise_word() -> WiseWordResponse:
    wise_word = await get_random_wise_word()
    return WiseWordResponse(
        content=wise_word.content,
        author=wise_word.author,
    )


@router.post("/")
async def api_add_bookmark(
        ids: BookMarkWiseWordRequest,
        current_user: User = Depends(get_current_user),
) -> dict:
    if ids.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bad token or bad user_id")
    user_id = current_user.id
    wise_word_id = ids.wise_word_id
    await add_bookmark(user_id=user_id, wise_word_id=wise_word_id)
    return {"message": "Bookmark added"}