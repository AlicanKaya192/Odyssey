import hashlib
import hmac

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
SALT = "odyssey-salt"
users = {
    "ada": "887362783edaec9e1b53b6e44e5e7fd3d15211a39abe696032db618b212115b3",
    "alan": "a90c9f1188728ecdf5e047af7c9411d05288916f59c7a7446aa4074b0f0fdf01",
}


def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()


class Login(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(form: Login):
    stored = users.get(form.username)
    if stored is None or not hmac.compare_digest(stored, hash_password(form.password, SALT)):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    return {"ok": True, "user": form.username}
