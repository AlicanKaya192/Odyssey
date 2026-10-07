from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
books = {}
next_id = 1

# BookIn (title en az 1, year 1450-2100), BookPatch (ikisi istege bagli), BookOut (+ id)
# POST /books (201), GET /books?year=, GET /books/{id}, PATCH /books/{id}, DELETE /books/{id} (204)
# bulunamazsa 404 "Book not found"; numara next_id ile (tekrar etmez)
