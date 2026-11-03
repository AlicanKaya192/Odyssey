A policy is made of statements with `effect` (`"allow"` / `"deny"`) and
`action` (may contain the `*` wildcard). `is_allowed(policy, action)` should
return `False` if any matching statement is `deny`, `True` if at least one
is `allow`, and `False` if none match. Matching: `fnmatch.fnmatchcase(action,
pattern)`. The starter code decides by the first matching statement.

**Expected output:**

```
True
False
False
```
