from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Item: name (metin), price (ondalik), qty (tam sayi, varsayilan 1)
# Order: customer (metin), items (Item listesi)
# POST /orders -> {"customer", "lines": kalem sayisi, "total": price*qty toplami, 2 basamak}
