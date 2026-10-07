from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    qty: int = 1


class Order(BaseModel):
    customer: str
    items: list[Item]


@app.post("/orders")
def place_order(order: Order):
    total = sum(item.price * item.qty for item in order.items)
    return {"customer": order.customer, "lines": len(order.items), "total": round(total, 2)}
