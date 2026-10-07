Turn the retry into a function; the wait doubles on each attempt, and there is
no waiting at all on errors that need fixing.

**What to do:**

1. Write the function `get_with_retry(url, attempts)`:
   - on each attempt it sends a request with `timeout=5`,
   - if the code is below 500 it **returns** the response at once (success
     or a 4xx),
   - on `5xx`, `Timeout` or `ConnectionError` it waits and tries again; the
     first wait is **0.5** seconds, doubling each time,
   - it does not wait after the last attempt; if the attempts run out it
     returns `None`.
2. Try three addresses and print the result: `/flaky` (4 attempts),
   `/books/99` (4 attempts), `/broken` (3 attempts). If there is a response
   print its code; if `None`, print `gave up`.

**Expected output:**

```
/flaky -> 200
/books/99 -> 404
/broken -> gave up
```

The check makes sure **only one** request was sent for `/books/99` and that
there were waits between the `/flaky` attempts.
