from fastapi import FastAPI, HTTPException

app = FastAPI()
books = {1: {"title": "Dune", "year": 1965}}


@app.get("/books")
def list_books():
    return books
