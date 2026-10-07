from contextlib import asynccontextmanager

from fastapi import FastAPI

stats = {"loads": 0}
words = set()


def load_words() -> set:
    stats["loads"] += 1
    return {"api", "python", "odyssey", "fastapi"}

app = FastAPI()


# lifespan: acilista words'u load_words() ile doldur (BIR KEZ), kapanista words.clear()
# GET /check?word=.. -> {"word", "known": kucuk harfli kelime words'te mi}
# GET /stats -> stats
