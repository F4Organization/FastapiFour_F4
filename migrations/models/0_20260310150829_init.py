from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
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
    "eJzdlW9P2zAQxr+K5VcgdaikDe36rjA2Oo12gu6PmKbITdzUwrGLfRlUrN99OidpmhQ6mJ"
    "gGe9Xm8Z1994tzzy1NdMSl3ftkuaE9cksVSzjtkYreIJTN56WKArCJdIGp5cYpbGLBsBBo"
    "j0yZtLxBaMRtaMQchFa0R1QqJYo6tGCEikspVeIq5QHomMPMFfLte4NQoSJ+w23xOL8Mpo"
    "LLqFKniPBspwewmDvtUMQDBW9dLB44CUIt00SV8fMFzLRaJQgFqMZcccOA4wlgUuwAC8w7"
    "LZrKii1DsirXciI+ZamEtY4fiCHUChEKBdjzLY3xlFevPa/V6njN1kHXb3c6frfZbRDqSt"
    "pc6iyzhksg2VYOy+DdYDjGRrVhYfb2UFi6HAYsy3K8S8DudwPx0YyZuwEX8TXEFkwdcQF0"
    "G+NCKCGXd+uJKCfsJpBcxTCjPeI3twD83D87Oumf7fjNXQethMQTJuRjKK0SngbTX7+KFU"
    "j7zYdQ2m9uYAoNx6YCBpus3jDgIBJ+N69qZg1alKfuFX+e6U0znEUjJRf5+9nCcDw4PT4f"
    "908/YieJtVfSIeqPj3HFc+qipu4c7Fa/7dUm5MtgfELwkVyMhseOoLYQG3diGTe+oFgTS0"
    "EHSl8HLFq7SoVagFniSJ7mI3k1oycsvLxmJgo2VrSn74vdXEq8pK4wxWL3WhAulpk7VJ8b"
    "Ec7u8q58Zat7sTLm2djXf+Rd3n670+62Dtory1op25zq9670gxuLJT1i5K6lvExv8nz/AW"
    "PX8/362MXr/whQefjLhPTn3qQV8OxbqoJ6fz4a3mNKZUrdkUQI5CeRwsLzhLa8nxH2W7Gd"
    "YUHttP+1ZjHDow+jw7qf4AaHdPlvDWL5C8tIGzA="
)
