from fastapi import APIRouter

from models import BookIn

router = APIRouter(prefix="/books", tags=["books"])
books = {}


@router.post("", status_code=201)
def add_book(book: BookIn):
    new_id = len(books) + 1
    books[new_id] = book.model_dump()
    return {"id": new_id, **books[new_id]}


@router.get("")
def list_books():
    return books
