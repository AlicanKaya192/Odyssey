`fetch_or_default(delay, limit)` should wait for `slow(delay)` at most
`limit` seconds: if it finishes in time, return its result (`"ok"`); if time
runs out, return the text `"timeout"`. Use `async with asyncio.timeout(limit):`
and `except TimeoutError`. Do not change the `check` wrapper.

**Expected output:**

```
ok timeout
```
