from fastapi import FastAPI

app = FastAPI()

# GET /search?q=... -> {"q": q, "length": q'nun uzunlugu}
# q zorunlu: gonderilmezse 422
