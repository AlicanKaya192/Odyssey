The order of the roles: `"user"` < `"moderator"` < `"admin"`.

`classify_attempt(user, user_role, owner, required_role)` should classify
an access attempt:

1. If `user_role` is **lower** than `required_role` → `"vertical"`.
2. Otherwise, if `owner` is not `None`, differs from `user`, and
   `user_role` is `"user"` → `"horizontal"`.
3. Every other case → `"allowed"`.

Use a dictionary such as `{"user": 1, "moderator": 2, "admin": 3}` to order
the roles; do not compare the texts directly with `<` (that gives
alphabetical order).

**Expected output:**

```
allowed
horizontal
vertical
allowed
```
