from fastapi import FastAPI

from routers import books, books_v2

app = FastAPI(title="Library")
app.include_router(books.router, prefix="/v1")
app.include_router(books_v2.router, prefix="/v2")
