from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()
items = {1: "pen", 2: "book"}
events = []


def get_conn():
    events.append("open")
    try:
        yield "conn"
    finally:
        events.append("close")


Conn = Annotated[str, Depends(get_conn)]


@app.get("/items")
def list_items(conn: Conn):
    return items


@app.get("/items/{item_id}")
def read_item(item_id: int, conn: Conn):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "name": items[item_id]}


@app.get("/events")
def show_events():
    return events
