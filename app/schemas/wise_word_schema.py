from pydantic import BaseModel

class WiseWordResponse(BaseModel):
    content: str
    author: str

class BookMarkWiseWordRequest(BaseModel):
    user_id: int
    wise_word_id: int