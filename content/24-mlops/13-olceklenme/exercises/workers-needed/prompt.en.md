Write the function `workers_needed(rate, service_ms, target)` that finds the fewest workers needed to keep the utilization below a target:

- Start with 1 worker.
- As long as the utilization (`rate × service_ms / 1000 / workers`) is greater than `target`, add a worker.
- Return the number of workers.

**Expected output:**

```
1
2
20
```
