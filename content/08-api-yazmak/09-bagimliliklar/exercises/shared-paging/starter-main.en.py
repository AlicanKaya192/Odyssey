from typing import Annotated

from fastapi import Depends, FastAPI, Query

app = FastAPI()
books = ["Dune", "Emma", "Ubik", "Kindred", "Beloved"]
movies = ["Alien", "Heat", "Up"]

# paging dependency: limit (1-5, default 2), offset (0 or more, default 0)
#   returns {"limit": .., "offset": ..}
# GET /books and GET /movies both return a slice using paging
