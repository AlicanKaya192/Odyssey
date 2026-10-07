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


@app.post("/products", status_code=201)
def add_product(product: ProductIn, db: DB):
    try:
        cur = db.execute("INSERT INTO products (name, price) VALUES (?, ?)", (product.name, product.price))
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Product already exists")
    return {"id": cur.lastrowid, **product.model_dump()}


@app.get("/products")
def list_products(db: DB, max_price: float | None = None):
    if max_price is None:
        rows = db.execute("SELECT id, name, price FROM products ORDER BY id").fetchall()
    else:
        rows = db.execute("SELECT id, name, price FROM products WHERE price <= ? ORDER BY id",
                          (max_price,)).fetchall()
    return [dict(r) for r in rows]


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: DB):
    cur = db.execute("DELETE FROM products WHERE id = ?", (product_id,))
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")
