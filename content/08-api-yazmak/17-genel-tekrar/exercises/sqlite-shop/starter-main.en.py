import sqlite3
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
DB_PATH = "shop.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL)""")
    conn.commit()
    conn.close()


init_db()


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


DB = Annotated[sqlite3.Connection, Depends(get_db)]


class ProductIn(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)


# POST /products (201) -> {"id", "name", "price"}; the same name -> 409 "Product already exists"
# GET /products?max_price= -> ordered by id; if max_price is given, price <= max_price (with ?!)
# DELETE /products/{id} -> 204; 404 "Product not found" if missing (rowcount 0)
