from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()
books = {}


class Book(BaseModel):
    title: str
    year: int


# POST /books -> 201, {"id", "title", "year"} ve Location: /books/<id> basligi
# GET /books/{book_id} -> kitap
