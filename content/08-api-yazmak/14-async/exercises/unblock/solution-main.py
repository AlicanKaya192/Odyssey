import asyncio
import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/report")
async def report():
    await asyncio.sleep(0.2)
    return {"rows": 120}
