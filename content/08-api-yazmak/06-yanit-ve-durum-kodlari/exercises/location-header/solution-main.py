from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()
books = {}


class Book(BaseModel):
    title: str
    year: int


@app.post("/books", status_code=201)
def add_book(book: Book, response: Response):
    new_id = len(books) + 1
    books[new_id] = book.model_dump()
    response.headers["Location"] = f"/books/{new_id}"
    return {"id": new_id, **books[new_id]}


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return books[book_id]
