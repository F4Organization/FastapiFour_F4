from app.repositories import diary_repository


async def create_diary(title: str, content: str):
    return await diary_repository.create_diary(title, content)


async def get_diaries(user_id: int):
    return await diary_repository.get_diaries(user_id)


async def get_diary(diary_id: int):
    return await diary_repository.get_diary(diary_id)


async def delete_diary(diary_id: int):
    return await diary_repository.delete_diary(diary_id)