import hashlib
import hmac
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

app = FastAPI()
SALT = "odyssey-salt"
users = {
    "ada": "887362783edaec9e1b53b6e44e5e7fd3d15211a39abe696032db618b212115b3",
    "alan": "a90c9f1188728ecdf5e047af7c9411d05288916f59c7a7446aa4074b0f0fdf01",
}
tokens = {}
bearer = HTTPBearer()


def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()


def check_password(username: str, password: str) -> bool:
    stored = users.get(username)
    return stored is not None and hmac.compare_digest(stored, hash_password(password, SALT))


class Login(BaseModel):
    username: str
    password: str


# POST /token: check_password tutmazsa 401 "Wrong username or password";
#   tutarsa secrets.token_hex(16) ile jeton uret, tokens[jeton] = ad,
#   {"access_token": jeton, "token_type": "bearer"} dondur
# current_user: HTTPBearer'dan gelen jeton tokens'ta yoksa 401 "Invalid token"; varsa adi dondur
# GET /me -> {"user": ad}
