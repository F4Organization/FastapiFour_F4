from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL,
    "nickname" VARCHAR(20),
    "is_active" BOOL NOT NULL DEFAULT True,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_users_email_133a6f" ON "users" ("email");
COMMENT ON TABLE "users" IS '사용자 인증 정보를 저장하는 Tortoise ORM 모델.';
        CREATE TABLE IF NOT EXISTS "bookmarkedwiseword" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "wise_word_id_id" INT NOT NULL REFERENCES "wiseword" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "token_blacklists" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(2048) NOT NULL UNIQUE,
    "expires_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_token_black_token_71be72" ON "token_blacklists" ("token");
COMMENT ON TABLE "token_blacklists" IS '로그아웃된 토큰을 저장해 재사용을 차단하는 모델.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "bookmarkedwiseword";
        DROP TABLE IF EXISTS "users";
        DROP TABLE IF EXISTS "token_blacklists";"""


MODELS_STATE = (
    "eJztWm1z2jgQ/isePiUzbQaICXDfgJKWNsANcS+dXjse2RagwUjUlkuYHv/9VsIv2BhqUk"
    "Ih9ReDV7uy9tFK+6xGPwpTZmHbvWoyNpkiZ4KtB+LiB+ZYhb+UHwWKphj+7NB6pRTQbBbp"
    "CAFHhi3NjFB/DvrzQN9wuYNMDhpDZLsYRBZ2TYfMOGEUpNSzbSFkJigSOopEHiXfPKxzNs"
    "J8jB1o+PcriAm18CN2g9fZRB8SbMddIPLbUq7zxUzKOpTfSkXxNUM3me1NaaQ8W/Axo6E2"
    "oVxIR5hiB3EsuueOJ4YvRuf7HHi0Gmmkshrimo2Fh8iz+Zq7GTEwGRX4wWhc6eBIfOV1ua"
    "RW1dr1jVoDFTmSUFJdrtyLfF8ZSgR6WmEp2xFHKw0JY4Sb6WDhrI74Jn5voIWTKU4HMW6Z"
    "ANPyTa+CP0loAyB3YRsIInCjgDoQuuCD1af2wp+4HVBqnW77Xmt0/xaeTF33my0hamht0V"
    "KW0kVCenFzKeQMlsNqxYSdKA8d7Z0iXpXP/V5bIshcPnLkFyM97XNBjAl5nOmUzXVkrcVY"
    "IA2AAc1oYj0XOzqx9L0WRtzo5wvkRGbxIGskgk7sZrrYzvbGL8XyTwJR7M7DSeo+40fWJp"
    "a3zMFkRD/ghYS0A4NC1MQp0PlZ6iP0dJoQLoNwCKTRUnXQPExaiVUGHoJfmEsfW437VuNN"
    "u7A1Hg8A4HpyP18QU5ZaOpIiKA1kTuYIdGPRKVpYmSUkoe5m07Q8TUoQRSOJg/BGjD0Jcg"
    "rPysauck51rpwK8vKYOZvYtcbISQcvskgACMM+zWUKkf+o25iO+FgAV6nsQOyfxqD1rjG4"
    "AK3LRKqFXjmmKdxTw49bAm3N5FzA2kUr25+0GKPsBWh1G58uY6zyrt97G6hHlLLXuus3k6"
    "jmpP7lkPoNUrU9oUUREJXmepgo3c1gaPrd3H4YYBtJoLfShvTTgdOb/m0EYvmc6V6S0pRU"
    "H5DV7WlekEE3U44vfPHMIjLheYPq8KzWi4r4qdbgWa9b4qVWqnzxDHOowrNeNaWoWBRaCB"
    "qsSgV0jXJdVTTmcAbzqPQHXdAyEBIt19XaVSGB8hE/m3OVo3MVPEXE3oeqhAaHSb7Pjt9h"
    "eMoYuWPYS2fIdQNOnhWwFNNz4S0HAo8ScyL/74Haus2T4PLj6PehVcwCVjGJFXF1yAHkew"
    "pYkIBtjOiWLW3dLgEYkAH7uQIsXK6HJsbNfv8uxsqanSTz/dhttgcXJUnHQImsCv/N87yc"
    "Dr8gOhw7455ZT5zYuGU+sb91YkN2/uQyJy9yohiI0OFsgqlu2OC/TVz+i9Boordm0NmZwf"
    "KctV8CmJQqcBO67fVg2qRlKQ2NWgVqNGQNRVlWUVVRr5nXIFdLoh6zSgjqMatYlVWZqm6U"
    "aFUpqspCL1burXTNsizhcC1Wzv2scDyNQeVl5dHLShnF+/D90OAsy8qiWsvE9tVaku/jxx"
    "mBvPkEChO3PACFOX7FdCaMJXB7JxfNi4wXwUW3XqTZ/xZNfvsjhmF+9SMeGqd0W6GBHWKO"
    "06ir37KTsqJIJ7+ncGKLchdJ+44d1y/5stK0NZM/7BBbhP8eQPnq5wlSqZjl8Bq0Ml/neH"
    "/f7+17ncMiJlf+U07+tCENI+Hv7msdyRscCeIiOmimJdVjJojl/zJblII="
)
