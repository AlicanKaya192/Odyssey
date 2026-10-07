from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
books = {
    1: {"title": "Dune", "year": 1965},
    2: {"title": "Emma", "year": 1815},
}


# Book modeli: title, year
# GET /books/{book_id} -> kitap ya da 404 "Book not found"
# PUT /books/{book_id} -> kitabin tamamini degistir, {"id", "title", "year"} dondur;
#   kitap yoksa 404
