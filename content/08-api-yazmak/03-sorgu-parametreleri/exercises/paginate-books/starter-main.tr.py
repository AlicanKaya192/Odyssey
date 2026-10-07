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

# GET /books?page=1&per_page=2
#   -> {"page", "per_page", "total", "items"}
#   page varsayilan 1, per_page varsayilan 2
