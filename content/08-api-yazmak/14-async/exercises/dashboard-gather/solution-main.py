import asyncio

from fastapi import FastAPI

app = FastAPI()


async def get_weather(city: str) -> dict:
    await asyncio.sleep(0.2)
    return {"city": city, "temp": 21}


async def get_news(city: str) -> list:
    await asyncio.sleep(0.2)
    return [f"{city} opens a new library", f"{city} marathon on Sunday"]


@app.get("/dashboard/{city}")
async def dashboard(city: str):
    weather, news = await asyncio.gather(get_weather(city), get_news(city))
    return {"weather": weather, "news": news}
