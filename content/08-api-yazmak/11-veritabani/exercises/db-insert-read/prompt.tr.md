`notes` tablosu ve `get_db` bağımlılığı hazır.

**Yapman gerekenler:**

1. `POST /notes`: notu `INSERT` et, `commit` et, `201` ile
   `{"id": ..., "text": ..., "pinned": ...}` döndür (`id` = `lastrowid`).
2. `GET /notes/{note_id}`: notu oku; yoksa `404` (`"Note not found"`).

SQLite'ta `bool` yok: `int(note.pinned)` ile `0`/`1` sakla, okurken
`bool(row["pinned"])`.

- `POST /notes` `{"text": "buy milk"}` → `201`, `{"id": 1, "text": "buy milk", "pinned": false}`
- `GET /notes/1` → aynı not
- `GET /notes/9` → `404`
