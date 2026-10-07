from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
prices = {"small": 10, "medium": 12, "large": 15}


class Order(BaseModel):
    size: Literal["small", "medium", "large"]
    qty: int = Field(default=1, ge=1, le=10)


@app.post("/orders")
def place_order(order: Order):
    return {"size": order.size, "qty": order.qty, "total": prices[order.size] * order.qty}
