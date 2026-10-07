from fastapi import FastAPI, HTTPException, status

app = FastAPI()
notes = {1: "buy milk", 2: "call mom", 3: "read Dune"}


@app.get("/notes")
def list_notes():
    return notes


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    del notes[note_id]
