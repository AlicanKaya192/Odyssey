from fastapi import FastAPI

app = FastAPI(title="Shop")

# routers.orders'i ekle; OutOfStock'u 409 {"error": "out_of_stock", "item": ...} cevabina ceviren yakalayici
