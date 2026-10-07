from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book(BaseModel):
    title: str = Field(examples=["Dune"], description="The book's title")
    year: int = Field(examples=[1965], description="Year of first publication")


@app.post("/books", status_code=201, tags=["books"])
def add_book(book: Book):
    return book


@app.get("/old-books", tags=["books"], deprecated=True)
def old_books():
    return []
