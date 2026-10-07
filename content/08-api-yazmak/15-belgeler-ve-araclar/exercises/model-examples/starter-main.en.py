from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# Book: title (example "Dune", description "The book's title"), year (example 1965, description "Year of first publication")
# POST /books -> 201, return the book, tags ["books"]
# GET /old-books -> [] ; tags ["books"], shown as deprecated in the docs
