from fastapi import FastAPI, HTTPException

app = FastAPI()
books = {
    1: {"id": 1, "title": "Dune", "year": 1965},
    2: {"id": 2, "title": "Emma", "year": 1815},
    3: {"id": 3, "title": "Ulysses", "year": 1922},
}

# GET /books/{book_id}: return the book; if missing, 404 "Book not found"
