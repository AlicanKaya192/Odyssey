from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
names = {"ada"}


class Signup(BaseModel):
    name: str


# POST /signup -> adi kucuk harfe cevir; names'te varsa 409,
#   detail {"code": "name_taken", "name": ad}; yoksa ekle, 201 {"name": ad}
