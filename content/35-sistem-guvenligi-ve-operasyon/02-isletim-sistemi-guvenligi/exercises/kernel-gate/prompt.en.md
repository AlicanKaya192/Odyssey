`policy` is role → list of allowed operations; the operations under the
`"everyone"` key are open to **everyone**. `allowed(role, operation,
policy)` should return `True` if the operation is in the role's list or in
the `"everyone"` list, and `False` otherwise. A role missing from the
policy must not raise an error: it is denied by default (only the
`"everyone"` operations are open).

**Expected output:**

```
True
False
True
False
```
