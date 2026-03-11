from fastapi import APIRouter
from app.models.wise_word_model import WiseWord
from app.schemas.wise_word_schema import WiseWordResponse
from app.services.wise_words_service import get_random_wise_word

router = APIRouter(prefix="/wise_words", tags=["WiseWords"])

@router.get("/")
async def api_get_random_wise_word() -> WiseWordResponse:
    wise_word = await get_random_wise_word()
    return WiseWordResponse(
        content=wise_word.content,
        author=wise_word.author,
    )
