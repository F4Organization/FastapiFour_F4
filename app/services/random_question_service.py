from app.models.random_question_model import RandomQuestion
from app.repositories.random_question_repository import RandomQuestionRepository

class RandomQuestionService:

    def __init__(self) -> None:
        self.repository = RandomQuestionRepository()

    #랜덤 질문 반환
    async def get_random_question(self):
        question = await self.repository.get_random_question()

        # 질문이 없을 시
        if not question:
            raise ValueError("질문이 없습니다.")

        return question

    # 질문 생성
    async def create_question(self, question: str):
        return await self.repository.create_question(question)

    # 질문 전체 조회

    async def get_all_questions(self):
        return await self.repository.get_all_questions()