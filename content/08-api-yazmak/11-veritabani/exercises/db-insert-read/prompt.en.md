The `notes` table and the `get_db` dependency are ready.

**What to do:**

1. `POST /notes`: `INSERT` the note, `commit`, return
   `{"id": ..., "text": ..., "pinned": ...}` with `201` (`id` = `lastrowid`).
2. `GET /notes/{note_id}`: read the note; `404` (`"Note not found"`) if
   missing.

SQLite has no `bool`: store `0`/`1` with `int(note.pinned)`, and read with
`bool(row["pinned"])`.

- `POST /notes` `{"text": "buy milk"}` → `201`, `{"id": 1, "text": "buy milk", "pinned": false}`
- `GET /notes/1` → the same note
- `GET /notes/9` → `404`
