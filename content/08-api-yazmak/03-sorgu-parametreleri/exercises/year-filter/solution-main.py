from fastapi import FastAPI

app = FastAPI()
books = [
    {"id": 1, "title": "Dune", "author": "Herbert", "year": 1965},
    {"id": 2, "title": "Emma", "author": "Austen", "year": 1815},
    {"id": 3, "title": "Ulysses", "author": "Joyce", "year": 1922},
    {"id": 4, "title": "Kindred", "author": "Butler", "year": 1979},
    {"id": 5, "title": "Persuasion", "author": "Austen", "year": 1817},
    {"id": 6, "title": "Beloved", "author": "Morrison", "year": 1987},
]


@app.get("/books")
def list_books(year_from: int | None = None):
    if year_from is None:
        return books
    return [book for book in books if book["year"] >= year_from]
