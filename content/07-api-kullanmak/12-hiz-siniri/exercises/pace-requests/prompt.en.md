This time do not hit the limit at all: space the requests out.

**What to do:**

1. Send 6 requests to `/limited`; after each request wait `GAP`.
2. Collect the codes into a `codes` list and print it.
3. If no 429 came, print `no 429`.

Choose the value of `GAP` yourself: 3 requests a second are allowed; the gap
must be a little above `1 / 3` of a second.

**Expected output:**

```
[200, 200, 200, 200, 200, 200]
no 429
```
