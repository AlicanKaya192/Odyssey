Each of four addresses ends differently. Handle them all with one function,
telling them apart by kind.

**What to do:**

1. Write the function `fetch(url)`. It calls `requests.get(url, timeout=1)`
   and then `raise_for_status()`, and returns one of:
   - `"ok 200"` (with the real code) when all is well,
   - `requests.Timeout` → `"timeout"`,
   - `requests.ConnectionError` → `"no connection"`,
   - `requests.HTTPError` → `"http error 404"` (with the real code).
2. For every address in the `urls` list, print the result.

Write the `except` blocks from specific to general.

**Expected output:**

```
ok 200
http error 404
timeout
no connection
```
