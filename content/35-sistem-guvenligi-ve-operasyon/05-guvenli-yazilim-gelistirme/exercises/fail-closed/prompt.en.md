`is_admin(user, roles)` should return `True` if the user's role is
`"admin"`. For a user who is not in `roles` it should **refuse**
(`False`). The starter code swallows every error for a missing user and
says `True`: failing open.

**Expected output:**

```
True
False
False
```
