from fastapi import FastAPI

app = FastAPI(title="Shop")

# add routers.orders; a handler turning OutOfStock into 409 {"error": "out_of_stock", "item": ...}
