from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Library API",
    version="2.0.0",
    description="Books of a small library.",
)
books = {1: {"title": "Dune", "year": 1965}}


@app.get("/books")
def list_books():
    return books
