from pydantic import BaseModel


class DiaryCreate(BaseModel):
    title: str
    content: str


class DiaryResponse(BaseModel):
    diary_id: int
    title: str | None
    content: str | None

    class Config:
        from_attributes = True

class DiaryUpdateRequest(BaseModel):
    diary_id: int
    title: str | None
    content: str | None

class GetDiaryRequest(BaseModel):
    diary_id: int