from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
books = {
    1: {"title": "Dune", "year": 1965},
    2: {"title": "Emma", "year": 1815},
}


# Book model: title, year
# GET /books/{book_id} -> the book, or 404 "Book not found"
# PUT /books/{book_id} -> replace the whole book, return {"id", "title", "year"};
#   404 if the book is missing
