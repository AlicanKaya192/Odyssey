from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
users = {}

# UserIn: name, password (gelen govde)
# UserOut: id, name (giden cevap; password YOK)
# POST /users -> 201, kaydi users'a koy (password dahil), UserOut ile dondur
# GET /users -> butun kullanicilar, UserOut listesi olarak
