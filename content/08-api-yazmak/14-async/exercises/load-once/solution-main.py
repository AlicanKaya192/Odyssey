from contextlib import asynccontextmanager

from fastapi import FastAPI

stats = {"loads": 0}
words = set()


def load_words() -> set:
    stats["loads"] += 1
    return {"api", "python", "odyssey", "fastapi"}


@asynccontextmanager
async def lifespan(app):
    words.update(load_words())
    yield
    words.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/check")
def check(word: str):
    return {"word": word, "known": word.lower() in words}


@app.get("/stats")
def show_stats():
    return stats
