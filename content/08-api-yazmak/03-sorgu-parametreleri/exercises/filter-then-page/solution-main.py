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
def list_books(author: str | None = None, page: int = 1, per_page: int = 2):
    found = books
    if author is not None:
        found = [book for book in found if book["author"] == author]
    start = (page - 1) * per_page
    return {"total": len(found), "titles": [book["title"] for book in found[start:start + per_page]]}
