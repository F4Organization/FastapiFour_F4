from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wiseword" ADD "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wiseword" DROP COLUMN "created_at";"""


MODELS_STATE = (
    "eJztlV1v2jAUhv9KlKsibVXL6Id2l1G2MpVQtdGoOk2RSUywSOzUdgao47/Px0nIBxCBVG"
    "lF2l3ynvfY5zxxfF7NiPk4FKcjIvCIcd/8bLyaFEVYPWzEPhgmiuMiAoJE41Cb58o1z11j"
    "ITnypNInKBRYST4WHiexJIwqlSZhCCLzlJHQoJASSl4S7EoWYDnFXAV+/lIyoT5eYJG/xj"
    "N3QnBYLZfovbXuymWstT6VX7URdhu7HguTiBbmeCmnjK7dhEpQA0wxRxLD8pInUD5Ul3Wa"
    "d5RWWljSEks5Pp6gJJSldvdk4DEK/FQ1QjcYwC4f2+edq871p8vOtbLoStbK1Sptr+g9Td"
    "QEbMdc6TiSKHVojAU3lCgIfJNdd4r4dnhFRg2gKrsOMMfVRDAXCoTFsXkjhhFauCGmgZwC"
    "uIuLBmI/rIfurfVwolwtja5ApVaVOD0kVVYOXuw4aKWUY4HVwMbpPTlQdCTESwiCndMaWE"
    "8tHVlmkbuh/S23M3UbpNeE3b0bfqlT5Rj6d9EWsDcqIkmEd8CtZNb4+lnqaf7wPmmbqgd/"
    "SMNldnM00e8Peo+ONbivfIIby+lBpF3Bn6snl63qF1gvYoz6zq0Br8bz0O5pgkzIgOsdC5"
    "/zbEJN6qdnLmVzF/mlSy5XczAruJ4ns9JFA8IYebM54r67EWFttsu7GYraUV1BFAX6swBc"
    "KDMbWhbmxJtuG2dZpHGYocLzf5Qd0Sj7jbmAkg6YZaWUY7mf32iYwfE/ZOin9uOEdH52tg"
    "ck5dp74n9/HNqHTnyfeNL4Y4REbPyc7wNaAyPot3ny14d8bZ7AAjD5/+mAWP0FBz8lRQ=="
)
