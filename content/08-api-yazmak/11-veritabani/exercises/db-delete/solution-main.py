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


@app.get("/notes")
def list_notes(db: DB):
    rows = db.execute("SELECT id, text FROM notes ORDER BY id").fetchall()
    return [dict(r) for r in rows]


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: DB):
    cur = db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Note not found")
