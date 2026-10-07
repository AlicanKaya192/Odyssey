import asyncio

from fastapi import FastAPI

app = FastAPI()


async def get_weather(city: str) -> dict:
    await asyncio.sleep(0.2)
    return {"city": city, "temp": 21}


async def get_news(city: str) -> list:
    await asyncio.sleep(0.2)
    return [f"{city} opens a new library", f"{city} marathon on Sunday"]


# GET /dashboard/{city} -> async def; get_weather ve get_news'i asyncio.gather ile AYNI ANDA bekle
#   {"weather": ..., "news": ...}
