Write the function `merge_state(required, runs)`. `required` holds the required check names; `runs` holds the results that came, oldest to newest, each `[name, status]`. A check can be run again: **each name's last result** counts.

- If one required check's last status is `"failure"`: `"blocked by NAME"` (the first failing one on the list).
- Otherwise, if one required check's last status is not `"success"` or `"skipped"` (also if it never came): `"waiting for NAME"` (the first on the list).
- If all are fine: `"ready"`.

**Expected output:**

```
waiting for test (3.12)
ready
blocked by test (3.13)
```
