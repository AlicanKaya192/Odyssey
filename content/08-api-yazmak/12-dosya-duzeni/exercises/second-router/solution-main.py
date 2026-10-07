from fastapi import FastAPI

from routers import authors, books

app = FastAPI(title="Library")
app.include_router(books.router)
app.include_router(authors.router)
