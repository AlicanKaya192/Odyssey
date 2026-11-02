A forum post dictionary: `id`, `author`, `locked`.
`can_edit_post(user, role, post)` should be `True`/`False` by these rules:

- if `role` is `"admin"` or `"moderator"`, they may edit every post,
- the author may edit their own post **if it is not locked**,
- nobody else may edit it.

The starter code only asks about the role; it forgot the object-level
question (who owns the post?).

**Expected output:**

```
ada True False
alan False False
grace True True
```
