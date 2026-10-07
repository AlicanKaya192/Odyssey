from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    year: int = Field(ge=1450, le=2100)
    pages: int = Field(gt=0)


@app.post("/books", status_code=201)
def add_book(book: Book):
    return book
