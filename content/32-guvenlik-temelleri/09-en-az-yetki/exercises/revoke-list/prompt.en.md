Find the privileges to suggest for removal in a review.

- `grants`: `[user, privilege]` lists.
- `last_used`: a dictionary from `"user:privilege"` to the date of last
  use (ISO); the key is missing if it was never used.

`revoke_list(grants, last_used, today, max_idle)` should return, as
`"user:privilege"` in alphabetical order, the privileges for which **more
than** `max_idle` days have passed since the last use, or which were never
used. The difference of two dates in days is `(d2 - d1).days`.

**Expected output:**

```
['ada:crm:write', 'alan:logs:read']
```
