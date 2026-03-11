import random
from app.models.wise_word_model import WiseWord, BookmarkedWiseWord
from fastapi import HTTPException


async def get_random_wise_word() -> WiseWord:
    wise_word_id = random.randint(31, 15206)
    wise_word = await WiseWord.filter(id=wise_word_id).first()
    if not wise_word:
        wise_word = await WiseWord.all().order_by("?").first()
    return wise_word


async def add_bookmark(user_id: int, wise_word_id: int) -> dict:
    wise_word = await BookmarkedWiseWord.filter(user_id=user_id, wise_word_id=wise_word_id).first()
    if wise_word:
        raise HTTPException(status_code=400, detail="Wise word already bookmarked")
    else:
        await BookmarkedWiseWord.create(user_id=user_id, wise_word_id=wise_word_id)
        return {"message": "Bookmarked successfully"}

