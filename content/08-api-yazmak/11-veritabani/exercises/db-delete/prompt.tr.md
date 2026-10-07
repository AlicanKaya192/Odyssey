Dört not hazır, `GET /notes` yazılı.

**Yapman gereken:** `DELETE /notes/{note_id}`: satırı sil, `commit`, `204`.
Hiç satır silinmediyse (`rowcount` `0`) `404` (`"Note not found"`).
Önce `SELECT` yapma.

- `DELETE /notes/3` → `204`
- `GET /notes` → 1, 2, 4
- `DELETE /notes/3` → `404`
