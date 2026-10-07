from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
books = {
    1: {"title": "Dune", "year": 1965},
    2: {"title": "Emma", "year": 1815},
}


class Book(BaseModel):
    title: str
    year: int


@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]


@app.put("/books/{book_id}")
def replace_book(book_id: int, book: Book):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    books[book_id] = book.model_dump()
    return {"id": book_id, **books[book_id]}
