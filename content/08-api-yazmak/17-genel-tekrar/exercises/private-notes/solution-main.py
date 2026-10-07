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


@app.post("/token")
def login(form: Login):
    if not check_password(form.username, form.password):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    token = secrets.token_hex(16)
    tokens[token] = form.username
    return {"access_token": token, "token_type": "bearer"}


def current_user(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]) -> str:
    if cred.credentials not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")
    return tokens[cred.credentials]


User = Annotated[str, Depends(current_user)]


@app.post("/notes", status_code=201)
def add_note(note: NoteIn, user: User):
    global next_id
    notes[next_id] = {"id": next_id, "owner": user, "text": note.text}
    next_id += 1
    return notes[next_id - 1]


@app.get("/notes")
def my_notes(user: User):
    return [n for n in notes.values() if n["owner"] == user]


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, user: User):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    if notes[note_id]["owner"] != user:
        raise HTTPException(status_code=403, detail="Not your note")
    del notes[note_id]
