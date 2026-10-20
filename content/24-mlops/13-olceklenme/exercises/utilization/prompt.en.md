Write the function `utilization(rate, service_ms, workers)` that computes a server's utilization:

- `rate`: requests per second, `service_ms`: one request's duration (milliseconds), `workers`: the number of workers.
- Utilization = `rate × service_ms / 1000 / workers`, rounded to three digits.

**Expected output:**

```
0.5
0.6
0.338
```
