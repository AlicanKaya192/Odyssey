Write the function `should_promote(candidate, current, min_gain)` that makes the gate's decision. `candidate` and `current` are measurement dictionaries (such as `{"accuracy": 0.82}`); `current` is `None` if no version is in production.

In order:

- If the candidate's measurements have no `"accuracy"`, `"keep"` (an unmeasured version doesn't go into production).
- If `current` is `None`, `"promote"` (the first version).
- If the candidate's accuracy is at least `min_gain` more than the one in production, `"promote"`.
- Otherwise `"keep"`.

**Expected output:**

```
promote
keep
promote
keep
```
