`conflicts` is a list of conflicting duty pairs (each pair is a
two-element list). `user_perms` is a dictionary from user to their list of
privileges.

`conflict_counts(user_perms, conflicts)` should count how many pairs each
user holds **both halves of**, and return a dictionary containing only the
users with at least one conflict.

**Expected output:**

```
{'ada': 2, 'grace': 1}
```
