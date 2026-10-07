from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()
items = ["apple", "bread", "cheese", "dates", "eggs", "flour", "grapes", "honey"]

# GET /items?limit=..&offset=..
#   limit: between 1 and 5, default 3
#   offset: 0 or more, default 0
#   return limit items from the items list starting at offset
