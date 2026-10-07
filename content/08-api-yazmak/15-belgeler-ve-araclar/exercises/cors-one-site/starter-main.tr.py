from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORSMiddleware: yalnizca https://library.example.com, yalnizca GET, butun basliklar


@app.get("/books")
def list_books():
    return ["Dune", "Emma"]
