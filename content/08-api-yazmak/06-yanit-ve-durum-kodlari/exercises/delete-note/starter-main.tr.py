from fastapi import FastAPI, HTTPException, status

app = FastAPI()
notes = {1: "buy milk", 2: "call mom", 3: "read Dune"}


@app.get("/notes")
def list_notes():
    return notes


# DELETE /notes/{note_id} -> 204 (govde yok); not yoksa 404 "Note not found"
