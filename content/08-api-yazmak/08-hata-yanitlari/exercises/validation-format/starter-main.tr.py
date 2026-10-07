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


# RequestValidationError yakalayicisi: 422, {"error": "invalid_input", "fields": [alan adlari]}
#   alan adi = loc'un ilk ogesi atilarak noktayla birlestirilmis hali
