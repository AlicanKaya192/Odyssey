from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
books = {}
next_id = 1


class Book(BaseModel):
    title: str = Field(min_length=1)
    year: int


@app.post("/books", status_code=201)
def add_book(book: Book):
    global next_id
    books[next_id] = book.model_dump()
    record = {"id": next_id, **books[next_id]}
    next_id += 1
    return record


@app.get("/books/{book_id}")
def read_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    del books[book_id]
