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
    if conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0] == 0:
        conn.executemany("INSERT INTO notes (text, pinned) VALUES (?, ?)",
                         [("buy milk", 0), ("call mom", 1), ("read Dune", 0), ("pay rent", 1)])
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


# GET /notes?pinned=true|false -> notes, ordered by id
#   all if pinned isn't given; otherwise WHERE pinned = ? (0/1)
#   each note {"id", "text", "pinned": bool}
