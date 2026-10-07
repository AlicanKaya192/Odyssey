from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI()

# Signup modeli: username, email
#   username: yalnizca harf ve rakam (bosluk, nokta yok); kucuk harfe cevrilsin
#   email: icinde @ olmali
# Kural bozulursa ValueError. POST /signup -> modeli dondur
