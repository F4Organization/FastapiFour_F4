from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "diaries" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        ALTER TABLE "bookmarkedwiseword" RENAME TO "bookmarked_wise_words";
        ALTER TABLE "wiseword" RENAME TO "wise_words";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wise_words" RENAME TO "wiseword";
        ALTER TABLE "bookmarked_wise_words" RENAME TO "bookmarkedwiseword";
        DROP TABLE IF EXISTS "diaries";"""


MODELS_STATE = (
    "eJztWl1z2jgU/SsenpKZ3QwQE2DfgJAt2wAd4m463e54hC1Ag5GoLZcwXf77Xgl/YGNTkx"
    "IKiV8MXN0r6x5dWecYfS/MmIkt56rJ2HSG7Ck2H4mDH5ltFv5QvhcommH4ssPrN6WA5vPQ"
    "Rxg4GloybBj46wsI0BcQIT3Q0OE2Mjg4jZDlYDCZ2DFsMueEUbBS17KEkRngSOg4NLmUfH"
    "WxztkY8wm2oeGff8FMqImfsOP/nE/1EcFWNAsihyvtOl/Opa1D+Z10FHcb6gaz3BkNnedL"
    "PmE08CaUC+sYU2wjjkX33HbF8MXovLT9jNYjDV3WQ9yIMfEIuRbfSDcjBgajAj8YjSMTHI"
    "u7/F4uqVW1dn2j1sBFjiSwVFfr9MLc14ESgZ5WWMl2xNHaQ8IY4mbYWCSrI76N3y20cDLD"
    "ySBGI2Ngml7olf8lDq0P5C5sfUMIblhQB0IXcjD71Fp6E7cDSq3TbT9oje4HkcnMcb5aEq"
    "KG1hYtZWldxqwXN5fCzmA5rBdN0Iny2NHeKeKn8rnfa0sEmcPHtrxj6Kd9LogxIZcznbKF"
    "jsyNGvOtPjDgGU6s62BbJ6a+18KIBv14gZzILB5kjYTQBc+zvfFLiHxLIIqn82ia+JzxKm"
    "sbyztmYzKm7/FSQtqBQSFq4ATovI3qI/R0mhCu/HLwreFStdEi2LRiqwwyhLwwlzm2Gg+t"
    "xm27kFqPBwBwc38/XxATlloykqIoh8iYLhD4RqpTtLAyi1kC3+2mWXkWtyCKxhIHkY0Yex"
    "zkBKqVjWDlrOp8WRXszBNmb2PXmiA7GbwwIgYgDPs0FyrU/pNuYTrmEwFcpbIDsb8bg9a7"
    "xuACvC5jmy30yjFNYJ8afkoptI2QcwFrF7Fsf9IinLLno9VtfLqM8Mr7fu9P3z0klb3Wfb"
    "8ZRzWn9a+H1m/RqvQtLayAVH0eLYam183d+wG2kAQ6lTgkvyI4velPoxCrl9zwJS1N2Ox9"
    "upq+0Qs6mG2PL3xxjSIy4HqD6nCt1ouK+KjW4Fqvm+JHrVT54g6NkQrXetWQpmJReCFoMC"
    "sV8B2W66qiMZszmEelP+iC1xAh0XJdrV0VYigf8bY5Vzk6V8EzRKx9qEoQcJjN98XxOwxP"
    "mSBnAs/SOXKchffkywpYQui58JYDgUeJMZXf90BtM+ZZcHl19OvQKmYBqxjHijg67AHkWw"
    "JYsAFbGNGUR9pmXAwwIAPWSxVYsFwPTYyb/f59hJU1O3Hm+7HbbA8uSpKOgRNZS//tN3o5"
    "HX5FdDjylntuPnNio5H5xP7SiQ3Y+bNlTi5ywhoI0eFsiqk+tCB/izj8J6HRRG9Nv7Mzhs"
    "UkyCb4J9G4hU6WZwbCSwrgWHUkSOHt+kkXxUmVm0UfD2sVEKrIHAltWlFVIVqNa7CrJSFK"
    "zRICUWoWq1KaquqWTq1KU1Wq3YjmXfsaZaljcS2iaX+knk9jULm2Prq2llW8j+gJAs5SWx"
    "fVWibJo9biogc/zQmQh2fwuGjkAXjc8WXjmdA2P+2dhDxXWq+CkKeeJ9r/MFF+CCaCYX4C"
    "Jloap3RoY03pE5hrwPXTCeuGpsjPapzamtzJ0Qi39noxHQS8sZf4+UmN/KRGTpjyV9Nva2"
    "K3Xh7mRDgnwq+dCDewTYxJIYEJey07qTAKfXImfGKLchcT/oZtx/vLIysX3gg5F4J3IDYs"
    "yn8PoDz38wSpVMxylAW8MkuGvx76vX0lg0kMrvynnPx/j0kYiXx3S4e4SojxFtFBM2lTPe"
    "YGsfofvjp39w=="
)
