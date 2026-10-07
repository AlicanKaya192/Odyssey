**Yapman gerekenler:**

1. `require_key` bağımlılığı: `X-Api-Key` başlığı `letmein` değilse
   `401` (`"Invalid API key"`).
2. `GET /health` → `{"status": "ok"}`: herkese açık.
3. `GET /admin/stats` → `{"users": 42}` ve `GET /admin/logs` →
   `["started", "ready"]`: ikisi de `dependencies=[...]` ile anahtar
   istesin.

- `GET /admin/stats` (başlıksız) → `401`
- `GET /admin/stats`, `X-Api-Key: letmein` → `{"users": 42}`
- `GET /health` → `200`
