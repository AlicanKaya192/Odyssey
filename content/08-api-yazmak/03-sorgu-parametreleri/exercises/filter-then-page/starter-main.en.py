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

# GET /books?author=...&page=...&per_page=...
#   -> {"total": the number of filtered books, "titles": the titles on that page}
