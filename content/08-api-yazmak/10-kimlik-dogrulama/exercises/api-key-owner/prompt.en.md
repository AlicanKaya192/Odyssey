The `KEYS` dictionary holds which key belongs to whom.

**What to do:**

1. `APIKeyHeader(name="X-API-Key", auto_error=False)`.
2. A `require_api_key` dependency: `401` (`"Invalid API key"`) if the key
   isn't in `KEYS`, otherwise it returns the owner's name.
3. `GET /reports` → `{"owner": ..., "reports": 3}`.

- no header → `401`
- `X-API-Key: k-ada-1` → `{"owner": "ada", "reports": 3}`
- `X-API-Key: k-alan-2` → `{"owner": "alan", "reports": 3}`
