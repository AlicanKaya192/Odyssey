from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
prices = {"small": 10, "medium": 12, "large": 15}

# Order model:
#   size: only "small", "medium", "large"
#   qty: between 1 and 10, default 1
# POST /orders -> {"size", "qty", "total": price * qty}
