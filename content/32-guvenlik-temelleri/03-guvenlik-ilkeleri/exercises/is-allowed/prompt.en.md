The `rules` dictionary goes from a username to the list of allowed
actions. `is_allowed(rules, user, action)` should return `True` if the user
is allowed that action.

The starter code seems to work, but it allows everything for a user who is
**not on the list at all**. Fix it so that it denies by default.

**Expected output:**

```
True
False
False
```
