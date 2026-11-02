Role hierarchy: the `parents` dictionary says which roles a role
**inherits from**. If it is `{"admin": ["editor"], "editor": ["viewer"]}`,
`admin` gets all of `editor`'s permissions, and `editor` all of
`viewer`'s.

`effective_permissions(role, role_perms, parents)` should return the
role's own permissions together with those of **every** role it inherits
from, without repeats and in alphabetical order. The inheritance can go
several levels deep. If there is a cycle (`a` → `b` → `a`), keep the
visited roles in a set so as not to loop for ever.

**Expected output:**

```
viewer read
editor read, write
admin delete, manage, read, write
```
