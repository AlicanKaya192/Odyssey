Capacity planning starts with three numbers: incoming requests, the
duration of the work, the number of workers.

## The calculation

- Utilization = requests per second × duration of the work (seconds) ÷
  number of workers.
- Example: 50 requests per second, 10 ms, 1 worker → 50 × 0.01 ÷ 1 = 0.5.
- Workers needed: add workers until the utilization drops below the
  target (for example 0.7).

## The lesson's simulation (work takes 10 ms on average)

| Utilization | Mean wait | p95 wait |
|---|---|---|
| 0.50 | 9.8 ms | 45.3 ms |
| 0.80 | 36.4 ms | 120.9 ms |
| 0.90 | 74.1 ms | 226.6 ms |
| 0.99 | 329.5 ms | 1131.2 ms |

## The same utilization, more workers (90%)

| Workers | Mean wait |
|---|---|
| 1 | 74.1 ms |
| 2 | 34.5 ms |
| 4 | 15.4 ms |

## Checklist

- Is the utilization target below 100%, with headroom?
- Is the server stateless (every copy gives the same answer)?
- Is the latency limit written with p95 (the mean hides the tail)?

## Don't

- Don't plan the server for 100% utilization; the wait explodes there.
- Don't keep customer information in the server's memory between
  requests; horizontal scaling breaks.
