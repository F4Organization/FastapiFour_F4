from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "wiseword" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "author" VARCHAR(255) NOT NULL,
    "content" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztlW9r2zAQxr9K8KsVttFm6Vr2Lgv7S+dAF9bCGEaxL7aILLnSeUlo892nk+PKjVuTQG"
    "EL7J393CPp7od0dxvkKgFhXl9xA1dKJ8G73m0gWQ72oxV72QtYUfgICcimwpkX1rWoXVOD"
    "msVo9RkTBqyUgIk1L5AraVVZCkGiiq2Ry9RLpeQ3JUSoUsAMtA38/GVlLhNYgql/i3k04y"
    "Aepsvd2U6PcFU47YvEj85Ip02jWIkyl95crDBT8t7NJZKaggTNEGh71CWlT9ltKq0rqjL1"
    "lirFxpoEZqwU2Ch3RwaxksTPZmNcgSmd8qp/MjgbnL95Ozi3FpfJvXK2rsrztVcLHYFwEq"
    "xdnCGrHA6j58ZKC0G32Y0yph+H51dsAbRpbwOscXURrAWP0F+bZ2KYs2UkQKaYEbjT0w5i"
    "P4aXo8/DyxfWdeTQeVR2V4TqkjxkNYHlExetseRQYHWwmXy4nlDSuTE3goSwpvVteH3kIq"
    "tN5GIcfqrtynaDqk2Eo4vxe0uVXvFs3riPJExZPF8wnUStiOqrp7ztUN7PtxUmWepYUcVU"
    "36a3DUHzOHus620inT2Pec//jndAHe83aEMp7dHyGksO5Rk/U8+j67/PbKjshwnp5Ph4B0"
    "jWtfNg+Pp9HO47GBIeY++uJ7hpPc5/A1oHI6q3e0BszwKqXxlMtdvFbfDXB8T6Dz6ijeU="
)
