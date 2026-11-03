`rate_limit(times, capacity, rate)` should apply the token bucket: the
bucket starts full with `capacity` tokens (time 0), `rate` tokens arrive
every second (at most `capacity`), each request spends one token. For each
request in `times`, write `+` if it got through and `-` if not, and return
the text. The starter code never refills the bucket.

**Expected output:**

```
+++--+-++--
++-++--
```
