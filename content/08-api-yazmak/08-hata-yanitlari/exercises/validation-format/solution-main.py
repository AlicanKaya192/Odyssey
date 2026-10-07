from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()


class Book(BaseModel):
    title: str = Field(min_length=1)
    year: int


@app.exception_handler(RequestValidationError)
def validation_handler(request: Request, exc: RequestValidationError):
    fields = [".".join(str(p) for p in e["loc"][1:]) for e in exc.errors()]
    return JSONResponse(status_code=422,
                        content={"error": "invalid_input", "fields": fields})


@app.post("/books", status_code=201)
def add_book(book: Book):
    return book


@app.get("/books")
def list_books(limit: int = 10):
    return {"limit": limit}
