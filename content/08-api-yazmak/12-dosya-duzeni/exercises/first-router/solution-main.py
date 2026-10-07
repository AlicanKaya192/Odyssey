from fastapi import FastAPI

from routers import books

app = FastAPI(title="Library")
app.include_router(books.router)
