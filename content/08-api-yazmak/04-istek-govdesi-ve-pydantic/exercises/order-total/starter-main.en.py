from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Item: name (string), price (float), qty (integer, default 1)
# Order: customer (string), items (a list of Item)
# POST /orders -> {"customer", "lines": number of items, "total": sum of price*qty, 2 decimals}
