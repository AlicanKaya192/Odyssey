The ready `Perm` flag has `READ`, `WRITE`, `EXECUTE`. Write the function
`can_do(granted, needed)`: both lists are permission **names**
(`["READ", "WRITE"]`). Turn the names into members with `Perm[name]`,
combine them with `|`, and return `True` if all needed permissions are within
the granted ones (`in`).

**Expected output:**

```
True
False
```
