The request records are a list: each is `{"ms": duration, "status": status code}`. Write the function `system_health(requests)` and return a dictionary:

- `"p95_ms"`: the p95 of the durations with the nearest-rank method (sort, take element number `ceil(0.95 * n)`).
- `"error_rate"`: the share of those with status 500 or above.
- `"rejected_rate"`: the share of those with status exactly 422 (requests breaking the schema).

The shares rounded to three digits.

**Expected output:**

```
p95: 250
errors: 0.2
rejected: 0.1
```
