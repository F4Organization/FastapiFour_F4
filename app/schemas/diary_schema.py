from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DiaryBase(BaseModel):
    title: str
    content: str

class DiaryCreate(DiaryBase):
    pass

class DiaryUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]

class DiaryOut(DiaryBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True