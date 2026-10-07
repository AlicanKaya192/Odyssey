Küçük raporlar hemen hazırlanıyor, büyükleri sıraya giriyor.

**Yapman gereken:** `POST /reports`:

- `rows` en fazla 1000 → `200`, `{"rows": ..., "status": "done"}`
- `rows` 1000'den fazla → `rows`'u `jobs` listesine ekle, `202`,
  `{"queued": true, "position": sıradaki yeri}`

- `{"rows": 50}` → `200`, `{"rows": 50, "status": "done"}`
- `{"rows": 5000}` → `202`, `{"queued": true, "position": 1}`
- `{"rows": 2000}` → `202`, `{"queued": true, "position": 2}`
- `{"rows": 0}` → `422`
