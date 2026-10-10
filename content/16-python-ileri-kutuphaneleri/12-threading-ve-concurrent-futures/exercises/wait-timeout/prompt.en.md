`finished_within(delays, limit)` should call `pool.submit(nap, d)` for each
delay and wait at most `limit` seconds with
`concurrent.futures.wait(futures, timeout=limit)`. Return the list
`[number of finished jobs, number of unfinished jobs]`. The starter code
waits for every job to the end.

**Expected output:**

```
[2, 1]
```
