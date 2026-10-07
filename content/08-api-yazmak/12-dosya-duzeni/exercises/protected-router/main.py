from fastapi import FastAPI

from routers import admin, books

app = FastAPI(title="Library")
app.include_router(books.router)
app.include_router(admin.router)
