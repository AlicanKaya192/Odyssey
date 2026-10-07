from fastapi import FastAPI, HTTPException

app = FastAPI()
books = {
    1: {"id": 1, "title": "Dune", "year": 1965},
    2: {"id": 2, "title": "Emma", "year": 1815},
    3: {"id": 3, "title": "Ulysses", "year": 1922},
}


@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]


@app.get("/books/latest")
def latest_book():
    newest = max(books.values(), key=lambda book: book["year"])
    return newest
