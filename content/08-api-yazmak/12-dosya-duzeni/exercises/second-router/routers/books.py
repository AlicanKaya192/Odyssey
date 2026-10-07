from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/books", tags=["books"])
books = {1: "Dune", 2: "Emma"}


@router.get("")
def list_books():
    return books


@router.get("/{book_id}")
def read_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": book_id, "title": books[book_id]}
