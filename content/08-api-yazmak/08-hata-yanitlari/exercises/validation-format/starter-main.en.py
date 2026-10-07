from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()


class Book(BaseModel):
    title: str = Field(min_length=1)
    year: int


@app.post("/books", status_code=201)
def add_book(book: Book):
    return book


@app.get("/books")
def list_books(limit: int = 10):
    return {"limit": limit}


# RequestValidationError handler: 422, {"error": "invalid_input", "fields": [field names]}
#   field name = loc without its first item, joined with dots
