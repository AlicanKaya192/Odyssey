`decide(srm_p, guard_ok, low, threshold)` in order: `"stop: SRM"` if the
SRM p is below 0.001, `"stop: guardrail"` if the guardrail is broken
(`guard_ok` False), `"ship"` if the lower end is at least the threshold,
`"unclear"` if it is above zero, otherwise `"no evidence"`. The starter code
skips the trust checks.

**Expected output:**

```text
ship
stop: SRM
```
