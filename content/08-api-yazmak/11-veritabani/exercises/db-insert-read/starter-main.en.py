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


# NoteIn: text (string), pinned (bool, default False)
# POST /notes -> INSERT, commit, 201 {"id": lastrowid, "text", "pinned"}
#   (SQLite has no bool: store 0/1 with int(note.pinned))
# GET /notes/{note_id} -> {"id", "text", "pinned": bool(...)}; 404 "Note not found" if missing
