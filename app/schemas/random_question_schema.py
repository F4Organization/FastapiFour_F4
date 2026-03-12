from pydantic import BaseModel

class RandomQuestionResponse(BaseModel):
    id : int
    question : str

class RandomQuestionCreate(BaseModel):
    question : str