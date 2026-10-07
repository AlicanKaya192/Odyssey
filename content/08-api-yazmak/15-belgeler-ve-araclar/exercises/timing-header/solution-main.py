import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}"
    response.headers["X-App-Version"] = "2.0.0"
    return response


@app.get("/books")
def list_books():
    return ["Dune", "Emma"]


@app.get("/authors")
def list_authors():
    return ["Herbert", "Austen"]
