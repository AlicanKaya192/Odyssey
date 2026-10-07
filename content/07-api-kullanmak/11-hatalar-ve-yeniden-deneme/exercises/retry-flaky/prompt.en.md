`/flaky` returns `503` (busy) for the first two requests, then answers.

**What to do:**

1. Build a loop of at most 5 attempts. On each attempt send a request with
   `timeout=5` and print the attempt number and the status code.
2. Leave the loop when `200` comes; otherwise **wait 1 second** before the
   next attempt (`time.sleep(1)`).
3. At the end print the `report` and `attempt` values from the report.

**Expected output:**

```
attempt 1 503
attempt 2 503
attempt 3 200
report: ready
after attempt: 3
```

The check also makes sure you really waited between requests.
