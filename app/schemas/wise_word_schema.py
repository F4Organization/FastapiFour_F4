from pydantic import BaseModel

class WiseWordResponse(BaseModel):
    content: str
    author: str
