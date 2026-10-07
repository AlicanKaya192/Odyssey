**What to do:**

1. A `Note` model: `text` (a required string), `pinned` (`bool`, default
   `False`).
2. `POST /notes`: add the note to the list and return `201` with
   `{"id": position, "text": ..., "pinned": ...}`. `id` is its position in the
   list (starting at 1).
3. `GET /notes`: return the added notes.

- `POST /notes`, body `{"text": "buy milk"}` → `201`, `{"id": 1, "text": "buy milk", "pinned": false}`
- `POST /notes`, body `{"text": "call mom", "pinned": true}` → `201`, `{"id": 2, ...}`
- `POST /notes`, body `{"pinned": true}` → `422`
- `GET /notes` → two notes
