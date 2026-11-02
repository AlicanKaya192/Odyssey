`abac_allow(subject, resource, action, hour)` should apply the hospital's
rule; try the rules in this order:

1. If the record's `sensitivity` is `"high"` and the subject's `mfa` is
   `False` → `False` (a sensitive record needs two-step login).
2. If `role` is `"doctor"` → `True` if the departments (`dept`) are the
   same.
3. If `role` is `"nurse"` → `True` if the departments are the same, the
   action is `"read"` and `7 <= hour < 19`.
4. Every other case → `False`.

The starter code is the rule from the lesson; it does not know the first
item.

**Expected output:**

```
True True
True False
```
