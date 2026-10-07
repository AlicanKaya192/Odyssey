from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()
books = {1: {"title": "Dune", "year": 1965}, 2: {"title": "Emma", "year": 1815}}

# get_book(book_id): kitap yoksa 404 "Book not found", varsa kitabi dondurur
# GET /books/{book_id} -> kitap
# GET /books/{book_id}/age?now=2026 -> {"title", "age": now - year}
# Iki uc nokta da kitabi get_book bagimliligindan alsin
