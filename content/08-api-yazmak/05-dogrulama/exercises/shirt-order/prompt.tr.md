`prices` sözlüğü hazır: `small` 10, `medium` 12, `large` 15.

**Yapman gereken:** `Order` modeli ve `POST /orders`.

- `size`: yalnızca `"small"`, `"medium"`, `"large"`
- `qty`: 1–10, varsayılan `1`
- Cevap: `{"size": ..., "qty": ..., "total": fiyat × adet}`

- `{"size": "large", "qty": 2}` → `{"size": "large", "qty": 2, "total": 30}`
- `{"size": "small"}` → `{"size": "small", "qty": 1, "total": 10}`
- `{"size": "huge"}` → `422`
- `{"size": "medium", "qty": 11}` → `422`
