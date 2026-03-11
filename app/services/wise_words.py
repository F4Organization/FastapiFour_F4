import random
from app.models.wise_word_model import WiseWord, BookmarkedWiseWord

async def get_random_wise_word() -> WiseWord:
    wise_word_id = random.randint(31, 15206)
    wise_word = await WiseWord.filter(id=wise_word_id).first()
    if not wise_word:
        wise_word = await WiseWord.all().order_by("?").first()
    return wise_word

