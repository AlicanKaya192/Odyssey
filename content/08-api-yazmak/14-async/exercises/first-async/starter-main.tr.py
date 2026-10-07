import asyncio

from fastapi import FastAPI

app = FastAPI()

# GET /slow?seconds=0.1 -> async def; await asyncio.sleep(seconds); {"waited": seconds}
