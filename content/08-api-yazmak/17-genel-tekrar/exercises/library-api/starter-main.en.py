from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
books = {}
next_id = 1

# BookIn (title at least 1, year 1450-2100), BookPatch (both optional), BookOut (+ id)
# POST /books (201), GET /books?year=, GET /books/{id}, PATCH /books/{id}, DELETE /books/{id} (204)
# 404 "Book not found" when missing; numbers come from next_id (never repeat)
