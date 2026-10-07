from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()
books = {1: {"title": "Dune", "year": 1965}, 2: {"title": "Emma", "year": 1815}}


def get_book(book_id: int) -> dict:
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]


CurrentBook = Annotated[dict, Depends(get_book)]


@app.get("/books/{book_id}")
def read_book(book: CurrentBook):
    return book


@app.get("/books/{book_id}/age")
def book_age(book: CurrentBook, now: int = 2026):
    return {"title": book["title"], "age": now - book["year"]}
