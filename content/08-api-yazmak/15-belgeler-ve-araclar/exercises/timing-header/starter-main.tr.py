import time

from fastapi import FastAPI, Request

app = FastAPI()

# Ara katman: her cevaba X-Process-Time (gecen sure, 4 basamak) ve X-App-Version: 2.0.0 ekle


@app.get("/books")
def list_books():
    return ["Dune", "Emma"]


@app.get("/authors")
def list_authors():
    return ["Herbert", "Austen"]
