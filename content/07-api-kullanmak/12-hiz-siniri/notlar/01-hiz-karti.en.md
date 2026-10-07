Working with rate limits, summed up.

## Headers

| Header | Meaning | Example |
|---|---|---|
| `X-RateLimit-Limit` | The total allowance in the window | `3` |
| `X-RateLimit-Remaining` | What is left | `0` |
| `X-RateLimit-Reset` | When the allowance renews (seconds or a timestamp) | `1712000000` |
| `Retry-After` | Seconds to wait after a `429`/`503` | `1` |

Headers arrive as text: `int(r.headers["Retry-After"])`.

## Working out the gap

| Limit | At least between requests |
|---|---|
| 3 a second | 0.34 s |
| 60 a minute | 1 s |
| 30 a minute | 2 s |
| 1000 an hour | 3.6 s |

The formula: `gap = window_seconds / allowed_requests`, plus a little margin.

## Pattern: pacing + a safety net

```python
import time

def get_paced(url, gap=0.4, attempts=5):
    for _ in range(attempts):
        r = requests.get(url, timeout=5)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 1)))
            continue
        time.sleep(gap)
        return r
    return None
```

## How 429 differs from the other 4xx codes

| | `429` | `400`, `401`, `404`... |
|---|---|---|
| Is the request right? | Yes | No |
| What to do | Wait, send the same one | Fix the request |
