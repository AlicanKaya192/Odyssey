You need to collect 6 successful responses from `/limited`. If a 429 comes,
wait for `Retry-After` and send the same request again.

**What to do:**

1. Send requests until the number of successful responses is 6.
2. If a `429` comes, wait `int(r.headers["Retry-After"])` seconds and print
   `waited`; on success increase the counter.
3. At the end print the number of successful responses and the total number
   of requests.

**Expected output:**

```
waited
successful: 6
requests: 7
```
