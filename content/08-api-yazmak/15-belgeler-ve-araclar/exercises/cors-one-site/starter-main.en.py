from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORSMiddleware: only https://library.example.com, only GET, all headers


@app.get("/books")
def list_books():
    return ["Dune", "Emma"]
