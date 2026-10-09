Reports are prepared in the background; the `reports` dictionary holds
each report's status.

**What to do:** `GET /reports/{report_id}`:

- No report → `404`, `detail` `{"code": "not_found"}`
- Not ready (`"pending"`) → `503`, `detail` `{"code": "not_ready"}` and a
  `Retry-After: 30` header (telling the client "try in 30 seconds")
- Ready → `{"id": ..., "status": "ready"}`

In the Using APIs module you read `Retry-After` as a client; now you're sending it.
