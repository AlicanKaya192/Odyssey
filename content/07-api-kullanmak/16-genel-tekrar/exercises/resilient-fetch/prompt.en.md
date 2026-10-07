A review of Sections 11 and 12: a request function that survives both a busy
server and a rate limit.

**What to do:**

1. Write the function `get(path)`: at most 5 attempts;
   - on `429` wait for `Retry-After`,
   - on `5xx` wait 1 second,
   - on any other code return the response;
   - return `None` when the attempts run out.
2. Ask for `/flaky` once and `/limited` 5 times in a row with `get`, and print
   each response's code.

**Expected output:**

```
/flaky 200
/limited 200
/limited 200
/limited 200
/limited 200
/limited 200
```
