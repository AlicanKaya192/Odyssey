from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()
items = {1: "pen", 2: "book"}
events = []

# get_conn: yield'li bagimlilik. Once events'e "open" ekle, "conn" ver,
#   uc nokta bitince (hata olsa da) "close" ekle (try/finally)
# GET /items -> items (get_conn kullanir)
# GET /items/{item_id} -> {"id", "name"}; yoksa 404 "Item not found" (get_conn kullanir)
# GET /events -> events listesi (get_conn KULLANMAZ)
