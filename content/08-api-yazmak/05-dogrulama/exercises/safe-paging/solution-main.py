from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()
items = ["apple", "bread", "cheese", "dates", "eggs", "flour", "grapes", "honey"]


@app.get("/items")
def list_items(limit: Annotated[int, Query(ge=1, le=5)] = 3,
               offset: Annotated[int, Query(ge=0)] = 0):
    return items[offset:offset + limit]
