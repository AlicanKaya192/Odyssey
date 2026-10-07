from typing import Annotated

from fastapi import Depends, FastAPI, Query

app = FastAPI()
books = ["Dune", "Emma", "Ubik", "Kindred", "Beloved"]
movies = ["Alien", "Heat", "Up"]


def paging(limit: Annotated[int, Query(ge=1, le=5)] = 2,
           offset: Annotated[int, Query(ge=0)] = 0):
    return {"limit": limit, "offset": offset}


Paging = Annotated[dict, Depends(paging)]


@app.get("/books")
def list_books(page: Paging):
    return books[page["offset"]:page["offset"] + page["limit"]]


@app.get("/movies")
def list_movies(page: Paging):
    return movies[page["offset"]:page["offset"] + page["limit"]]
