from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://library.example.com"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/books")
def list_books():
    return ["Dune", "Emma"]
