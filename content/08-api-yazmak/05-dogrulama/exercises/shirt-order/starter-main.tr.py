from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
prices = {"small": 10, "medium": 12, "large": 15}

# Order modeli:
#   size: yalnizca "small", "medium", "large"
#   qty: 1-10 arasi, varsayilan 1
# POST /orders -> {"size", "qty", "total": fiyat * adet}
