import asyncio

from fastapi import FastAPI

app = FastAPI()


@app.get("/slow")
async def slow(seconds: float = 0.1):
    await asyncio.sleep(seconds)
    return {"waited": seconds}
