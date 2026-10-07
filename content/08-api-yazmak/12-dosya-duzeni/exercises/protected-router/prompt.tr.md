`deps.py`'de `require_key` bağımlılığı hazır (`X-Api-Key: letmein`).

**Yapman gereken:** `routers/admin.py`'deki router'ın **bütün** uç noktaları
anahtar istesin. Her uç noktaya ayrı ayrı değil, router'a bir kez yaz.

- `GET /admin/stats` (anahtarsız) → `401`
- `GET /admin/stats`, `X-Api-Key: letmein` → `{"books": 2}`
- `POST /admin/reset` (anahtarsız) → `401`
- `GET /books` anahtarsız çalışmaya devam ediyor
