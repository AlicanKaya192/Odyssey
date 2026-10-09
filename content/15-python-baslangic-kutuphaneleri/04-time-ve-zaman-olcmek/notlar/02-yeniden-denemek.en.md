Code that fetches data from the internet, connects to a database or waits for
another program sometimes hits a temporary error: the server is busy at that
moment, the network dropped for an instant. With such errors, instead of
giving up at once, **waiting a little and trying again** is a common pattern.

## Exponential backoff

After each failed attempt the waiting time **doubles**: 1, 2, 4, 8... If the
server is really struggling, everyone retrying at the same moment makes it
worse; waits that grow longer give it room to breathe.

```python
import time


def retry(func, attempts=5, base=0.01):
    waits = []
    for attempt in range(attempts):
        try:
            return func(), waits
        except ConnectionError:
            if attempt == attempts - 1:
                raise
            wait = base * 2 ** attempt
            waits.append(wait)
            time.sleep(wait)


calls = {"n": 0}


def flaky():
    calls["n"] += 1
    if calls["n"] < 4:
        raise ConnectionError("server busy")
    return "ok"


print(retry(flaky))
print(calls["n"])
```

```text
('ok', [0.01, 0.02, 0.04])
4
```

`flaky` fails on the first three calls and works on the fourth. `retry`
waited 0.01, 0.02 and 0.04 seconds after each error and returned the result
on the fourth attempt. If the last attempt fails too, `raise` passes the
error up: retrying forever is also a mistake.

We kept the times short in the example; in real programs the base is usually
0.5–1 second and the wait is cut by an upper limit (`min(limit, ...)`): with
a base of 1 second you would wait 2⁸ = 256 seconds, more than 4 minutes,
before the tenth attempt.

## What to retry?

- **Temporary** errors: the connection dropped, a timeout, "server busy"
  (HTTP `503`, `429`).
- **Permanent** errors are not retried: a wrong address (`404`), no
  permission (`401`), a `TypeError` in your code. However many times you try,
  the result is the same.

Catch only temporary errors on the `except` line (`ConnectionError`,
`TimeoutError`); a bare `except:` retries every error and hides the real one.
