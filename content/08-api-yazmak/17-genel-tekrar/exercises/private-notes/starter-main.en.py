import hashlib
import hmac
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

app = FastAPI()
bearer = HTTPBearer()
users = {
    "ada": "887362783edaec9e1b53b6e44e5e7fd3d15211a39abe696032db618b212115b3",
    "alan": "a90c9f1188728ecdf5e047af7c9411d05288916f59c7a7446aa4074b0f0fdf01",
}
tokens = {}
notes = {}
next_id = 1


def check_password(username: str, password: str) -> bool:
    stored = users.get(username)
    if stored is None:
        return False
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), b"odyssey-salt", 100_000).hex()
    return hmac.compare_digest(stored, digest)


class Login(BaseModel):
    username: str
    password: str


class NoteIn(BaseModel):
    text: str = Field(min_length=1)


# POST /token: login -> a token (secrets.token_hex(16)); 401 if wrong
# current_user: the HTTPBearer token -> the username; 401 if invalid
# POST /notes (201): {"id", "owner": user, "text"}
# GET /notes: ONLY the user's own notes
# DELETE /notes/{id}: 404 if missing, 403 "Not your note" if someone else's, otherwise 204
