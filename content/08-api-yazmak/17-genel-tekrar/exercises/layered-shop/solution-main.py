from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from errors import OutOfStock
from routers import orders

app = FastAPI(title="Shop")
app.include_router(orders.router)


@app.exception_handler(OutOfStock)
def out_of_stock(request: Request, exc: OutOfStock):
    return JSONResponse(status_code=409, content={"error": "out_of_stock", "item": exc.item})
