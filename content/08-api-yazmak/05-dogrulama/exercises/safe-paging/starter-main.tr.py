from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()
items = ["apple", "bread", "cheese", "dates", "eggs", "flour", "grapes", "honey"]

# GET /items?limit=..&offset=..
#   limit: 1-5 arasi, varsayilan 3
#   offset: 0 ya da buyuk, varsayilan 0
#   items listesinden offset'ten baslayarak limit kadar oge dondur
