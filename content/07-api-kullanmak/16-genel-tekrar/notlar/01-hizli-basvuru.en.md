All of the Using APIs module on one page.

## requests

| Job | Code |
|---|---|
| Get | `requests.get(url, params=..., headers=..., timeout=10)` |
| Create | `requests.post(url, json=..., headers=AUTH)` → `201` |
| Change part | `requests.patch(url, json=..., headers=AUTH)` → `200` |
| Replace | `requests.put(url, json=..., headers=AUTH)` → `200` |
| Delete | `requests.delete(url, headers=AUTH)` → `204` |
| Session | `s = requests.Session(); s.headers.update({...})` |
| Code | `r.status_code`, `r.ok`, `r.raise_for_status()` |
| Body | `r.json()`, `r.text` |
| Where it went | `r.url`, `r.request.headers` |

## Identity

| Method | Header |
|---|---|
| API key | `X-API-Key: ...` (the API picks the name) |
| Bearer | `Authorization: Bearer <token>` |
| Basic | `auth=(name, password)` |

The key: `os.environ.get("NAME")`; `.env` never goes into git.

## Codes

`200` OK · `201` created · `204` OK without a body · `400` broken request ·
`401` not recognised · `403` not allowed · `404` not there ·
`405` no such method here · `422` invalid values · `429` slow down ·
`500` server error · `503` not available right now

## Pagination

| Form | Stopping condition |
|---|---|
| `page` | `page >= meta.pages` or an empty page |
| `next` | `links.next` is `None` |
| `offset` + `limit` | `offset >= total` |
| `cursor` | `next_cursor` is `None` |

## Resilience

- A `timeout` on every request.
- Retry: `Timeout`, `ConnectionError`, `5xx`, `429` (`Retry-After`).
- Do not retry: `4xx`; an automatic `POST`.
- Waiting: 1, 2, 4... seconds; an upper limit.
- Pace: at least `window / allowance` seconds between requests.

## The data pipeline

Fetch → store (cache) → flatten → check (`assert`) → write (`"w"`). Updates
are incremental: `since` + merge by identifier.
