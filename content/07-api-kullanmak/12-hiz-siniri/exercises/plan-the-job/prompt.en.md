Work out how long a big data-pulling job will take before you start it. There
are no requests here; just arithmetic.

**What to do:**

1. Write the function `min_gap(allowed, window_seconds)`: it returns the
   shortest time between requests in seconds, **rounded** to two decimals
   (`round(..., 2)`).
2. Write the function `job_minutes(total_requests, allowed, window_seconds)`:
   it returns at least how many minutes the job takes, rounded to one decimal.
   (Total time = number of requests × the shortest gap; use the gap before
   rounding.)
3. For every job in the `jobs` list, print the gap and the duration.

**Expected output:**

```
500 requests: gap 1.0 s, at least 8.3 min
120 requests: gap 0.33 s, at least 0.7 min
10000 requests: gap 3.6 s, at least 600.0 min
```
