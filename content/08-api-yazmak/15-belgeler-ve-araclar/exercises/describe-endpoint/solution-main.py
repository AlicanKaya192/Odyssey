from fastapi import FastAPI, HTTPException

app = FastAPI(title="Library API")
books = {1: {"title": "Dune", "year": 1965}}


@app.get("/books/{book_id}", tags=["books"], summary="Read one book",
         responses={404: {"description": "No book with this id"}})
def read_book(book_id: int):
    """Returns the book with the given id."""
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]
