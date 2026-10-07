Four notes are ready and `GET /notes` is written.

**What to do:** `DELETE /notes/{note_id}`: delete the row, `commit`, `204`.
If no row was deleted (`rowcount` `0`), `404` (`"Note not found"`). Don't
`SELECT` first.

- `DELETE /notes/3` → `204`
- `GET /notes` → 1, 2, 4
- `DELETE /notes/3` → `404`
