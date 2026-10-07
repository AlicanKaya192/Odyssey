`/limited` allows 3 requests a second. Hit the limit on purpose and see what
the server says.

**What to do:**

1. Send 5 requests to `/limited` in a row (without waiting).
2. For each request print its number, the status code and the
   `X-RateLimit-Remaining` header.
3. At the end print how many requests got a `429`.

**Expected output:**

```
1 200 remaining 2
2 200 remaining 1
3 200 remaining 0
4 429 remaining 0
5 429 remaining 0
too many: 2
```
