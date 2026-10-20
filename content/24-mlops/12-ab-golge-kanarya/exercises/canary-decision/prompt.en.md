Write the function `canary_decision(n, min_n, canary_score, control_score, tolerance)` that decides a canary stage:

- If the canary has fewer than `min_n` customers, return `"wait"` (too early to decide).
- If the canary's score is less than `control_score - tolerance`, return `"rollback"`.
- Otherwise `"advance"`.

The checks are done in this order.

**Expected output:**

```
wait
rollback
advance
```
