import sqlite3
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
DB_PATH = "notes.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        pinned INTEGER NOT NULL DEFAULT 0)""")
    conn.commit()
    conn.close()


init_db()


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


DB = Annotated[sqlite3.Connection, Depends(get_db)]


class NoteIn(BaseModel):
    text: str
    pinned: bool = False


@app.post("/notes", status_code=201)
def create_note(note: NoteIn, db: DB):
    cur = db.execute("INSERT INTO notes (text, pinned) VALUES (?, ?)", (note.text, int(note.pinned)))
    db.commit()
    return {"id": cur.lastrowid, **note.model_dump()}


@app.get("/notes/{note_id}")
def read_note(note_id: int, db: DB):
    row = db.execute("SELECT id, text, pinned FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"id": row["id"], "text": row["text"], "pinned": bool(row["pinned"])}
