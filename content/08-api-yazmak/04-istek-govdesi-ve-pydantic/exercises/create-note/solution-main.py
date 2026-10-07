from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
notes = []


class Note(BaseModel):
    text: str
    pinned: bool = False


@app.post("/notes", status_code=201)
def add_note(note: Note):
    notes.append(note)
    return {"id": len(notes), **note.model_dump()}


@app.get("/notes")
def list_notes():
    return notes
