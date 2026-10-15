The canary's share is raised step by step. Write the function `ramp(old, stages, max_increase=0.01, min_requests=500)`:

- `old` is the old version's `[errors, requests]` counts.
- `stages` is the list of steps; each step is `[share, errors, requests]`, the share as a percentage (`5`, `25`...).

Go through the steps in order:

- If the requests are fewer than `min_requests`: return something like `"waiting at 5%"`.
- If the new error rate is greater than the old rate + `max_increase`: return something like `"rolled back at 25%"`.
- If all steps passed: `"fully promoted"`.

**Expected output:**

```
fully promoted
rolled back at 25%
waiting at 5%
```
