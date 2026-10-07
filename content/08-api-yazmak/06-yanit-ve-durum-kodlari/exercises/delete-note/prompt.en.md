The `notes` dictionary and `GET /notes` are ready.

**What to do:** `DELETE /notes/{note_id}` deletes the note and returns `204`
with no body. If the note is missing, `404` (`"Note not found"`).

- `DELETE /notes/2` → `204`
- `GET /notes` → `{"1": "buy milk", "3": "read Dune"}`
- `DELETE /notes/2` → `404`

`raise HTTPException(status_code=404, detail="...")` sends an error answer
(details in the Error Responses section).
