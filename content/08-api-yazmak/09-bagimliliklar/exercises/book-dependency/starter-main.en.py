from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()
books = {1: {"title": "Dune", "year": 1965}, 2: {"title": "Emma", "year": 1815}}

# get_book(book_id): 404 "Book not found" if missing, otherwise returns the book
# GET /books/{book_id} -> the book
# GET /books/{book_id}/age?now=2026 -> {"title", "age": now - year}
# Both endpoints get the book from the get_book dependency
