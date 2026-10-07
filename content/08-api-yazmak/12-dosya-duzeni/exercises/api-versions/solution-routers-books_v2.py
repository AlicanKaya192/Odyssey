from fastapi import APIRouter

from routers.books import books

router = APIRouter(prefix="/books", tags=["books v2"])


@router.get("")
def list_books():
    return [{"id": book_id, "title": title} for book_id, title in books.items()]
