Error handling on one page.

## Exceptions

| Exception | When | Retry? |
|---|---|---|
| `requests.Timeout` | No response within `timeout` | Yes |
| `requests.ConnectionError` | The server could not be reached | Yes |
| `requests.HTTPError` | `raise_for_status()` saw a 4xx/5xx | 5xx yes, 4xx no |
| `requests.RequestException` | The ancestor of them all | It depends |

## The order of catching

```python
try:
    r = requests.get(url, timeout=5)
    r.raise_for_status()
except requests.Timeout:
    ...
except requests.ConnectionError:
    ...
except requests.HTTPError:
    ...
except requests.RequestException:
    ...
```

From specific to general. `RequestException` last.

## A retry template

```python
import time

def get_with_retry(url, attempts=4):
    delay = 1
    for attempt in range(attempts):
        try:
            r = requests.get(url, timeout=5)
            if r.status_code < 500:
                return r
        except (requests.Timeout, requests.ConnectionError):
            pass
        if attempt < attempts - 1:
            time.sleep(delay)
            delay *= 2
    return None
```

## Rules

1. A `timeout=` on every request.
2. Retry only temporary errors: timeouts, connection errors, `5xx`, `429`.
3. Retry only idempotent requests: `GET`, `PUT`, `DELETE`.
4. Set an upper limit; double the wait on each attempt (1, 2, 4...).
5. On `429` and `503`, follow `Retry-After` if it is there.
6. When you give up, say clearly what happened.
