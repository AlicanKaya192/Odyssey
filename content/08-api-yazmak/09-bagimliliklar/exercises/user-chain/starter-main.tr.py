from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
users = {"ada": "admin", "alan": "member"}

# get_user: X-User basligi users'ta yoksa 401 "Unknown user"; varsa {"name", "role"}
# require_admin: get_user'a bagimli; rol "admin" degilse 403 "Admins only"; kullaniciyi dondurur
# GET /me -> kullanici (her kullanici)
# GET /admin -> {"welcome": ad} (yalnizca admin)
