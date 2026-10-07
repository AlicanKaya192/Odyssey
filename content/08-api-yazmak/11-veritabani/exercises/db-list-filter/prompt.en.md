Four notes are ready in the table (`init_db` adds them); 2 and 4 are pinned.

**What to do:** `GET /notes` with an optional `pinned` query. Notes ordered
by `id`; each one `{"id": ..., "text": ..., "pinned": true/false}`.

- `GET /notes` → four notes
- `GET /notes?pinned=true` → `[{"id": 2, "text": "call mom", "pinned": true}, {"id": 4, ...}]`
- `GET /notes?pinned=false` → 1 and 3
