Tabloda dört not hazır (`init_db` ekliyor); 2 ve 4 sabitlenmiş
(`pinned`).

**Yapman gereken:** `GET /notes`, isteğe bağlı `pinned` sorgusuyla. Notlar
`id` sırasıyla; her biri `{"id": ..., "text": ..., "pinned": true/false}`.

- `GET /notes` → dört not
- `GET /notes?pinned=true` → `[{"id": 2, "text": "call mom", "pinned": true}, {"id": 4, ...}]`
- `GET /notes?pinned=false` → 1 ve 3
