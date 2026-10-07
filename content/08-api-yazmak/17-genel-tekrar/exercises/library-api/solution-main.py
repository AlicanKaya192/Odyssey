from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
books = {}
next_id = 1


class BookIn(BaseModel):
    title: str = Field(min_length=1)
    year: int = Field(ge=1450, le=2100)


class BookPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    year: int | None = Field(default=None, ge=1450, le=2100)


class BookOut(BookIn):
    id: int


def find_book(book_id: int) -> dict:
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: BookIn) -> BookOut:
    global next_id
    record = {"id": next_id, **book.model_dump()}
    books[next_id] = record
    next_id += 1
    return record


@app.get("/books")
def list_books(year: int | None = None) -> list[BookOut]:
    result = list(books.values())
    if year is not None:
        result = [b for b in result if b["year"] == year]
    return result


@app.get("/books/{book_id}")
def read_book(book_id: int) -> BookOut:
    return find_book(book_id)


@app.patch("/books/{book_id}")
def update_book(book_id: int, patch: BookPatch) -> BookOut:
    record = find_book(book_id)
    record.update(patch.model_dump(exclude_unset=True))
    return record


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    find_book(book_id)
    del books[book_id]
