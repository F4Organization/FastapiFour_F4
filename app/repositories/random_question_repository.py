from app.models.random_question_model import RandomQuestion
from app.schemas.random_question_schema import RandomQuestionResponse


class RandomQuestionRepository:
    async def get_random_question(self) -> RandomQuestion:
        return await RandomQuestion.all().order_by('?').first()

    async def create_question(self, question: str)-> RandomQuestion:
        return await RandomQuestion.create(question=question)

    async def get_all_questions(self):
        return await RandomQuestion.all()