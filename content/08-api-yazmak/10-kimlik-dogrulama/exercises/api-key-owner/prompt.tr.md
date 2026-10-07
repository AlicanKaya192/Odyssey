`KEYS` sözlüğü hangi anahtarın kime ait olduğunu tutuyor.

**Yapman gerekenler:**

1. `APIKeyHeader(name="X-API-Key", auto_error=False)`.
2. `require_api_key` bağımlılığı: anahtar `KEYS`'te yoksa `401`
   (`"Invalid API key"`), varsa sahibinin adını döndürsün.
3. `GET /reports` → `{"owner": ..., "reports": 3}`.

- başlıksız → `401`
- `X-API-Key: k-ada-1` → `{"owner": "ada", "reports": 3}`
- `X-API-Key: k-alan-2` → `{"owner": "alan", "reports": 3}`
