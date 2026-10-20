Write the function `decide_month(live, base, drift, invalid, candidate)` for the decision part of the lesson's `run_month`. The thresholds are ready in the starter code. In order:

- If `live` is at least `base - MAX_DROP` and `drift` is at most `MAX_DRIFT`, return `"keep"`.
- If `invalid` (the share of invalid rows) is greater than `MAX_INVALID`, return `"data rejected"`.
- If `candidate` (the candidate's score) is less than `live + MIN_GAIN`, return `"kept out"`.
- Otherwise `"promoted"`.

**Expected output:**

```
keep
promoted
kept out
data rejected
```
