`broad_permissions(policy)` should return, **once each** and in
alphabetical order, the actions of `allow` statements whose action is
exactly `"*"` or ends with `":*"`. `deny` statements do not count: a broad
deny is not a problem.

**Expected output:**

```
['*', 'compute:*']
```
