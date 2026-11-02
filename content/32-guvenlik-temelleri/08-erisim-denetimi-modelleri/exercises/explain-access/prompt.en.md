A question often asked in an access review: "**why** can Ada do this?"
`explain_access(user, permission, user_roles, role_perms)` should return,
in alphabetical order, which of the user's roles give that permission. An
empty list if none does or the user is unknown.

**Expected output:**

```
['admin', 'teacher']
[]
```
