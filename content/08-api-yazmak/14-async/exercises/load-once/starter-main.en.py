from contextlib import asynccontextmanager

from fastapi import FastAPI

stats = {"loads": 0}
words = set()


def load_words() -> set:
    stats["loads"] += 1
    return {"api", "python", "odyssey", "fastapi"}

app = FastAPI()


# lifespan: at startup fill words with load_words() (ONCE), at shutdown words.clear()
# GET /check?word=.. -> {"word", "known": is the lower-cased word in words}
# GET /stats -> stats
