import time

from fastapi import FastAPI, Request

app = FastAPI()

# Middleware: add X-Process-Time (elapsed time, 4 decimals) and X-App-Version: 2.0.0 to every answer


@app.get("/books")
def list_books():
    return ["Dune", "Emma"]


@app.get("/authors")
def list_authors():
    return ["Herbert", "Austen"]
