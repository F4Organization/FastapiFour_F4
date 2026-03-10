from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url="postgres://user:password@localhost:5432/dbname",     # 유저, 디비이름 
        modules={"models": ["app.models"]}
    )
    await Tortoise.generate_schemas()