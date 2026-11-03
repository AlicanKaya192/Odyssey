`can_view(user, invoice)` should return whether the user may see the
invoice. `user` is a dict: `name`, `role`. The invoice is open to its owner
(`owner`) or to a user whose role is `"admin"`; closed to everyone else.
The starter code says `True` to everyone: horizontal escalation.

**Expected output:**

```
True
False
True
```
