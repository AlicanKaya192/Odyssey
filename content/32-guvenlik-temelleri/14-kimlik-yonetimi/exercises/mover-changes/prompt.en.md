`roles` is a dictionary from role name to a list of permissions. An
employee's role changes from `old_role` to `new_role`.

`mover_changes(old_role, new_role, roles)` should return a dictionary:
`"add"` the permissions in the new role but not the old, `"remove"` those
in the old but not the new; both lists in alphabetical order. Permissions
in both roles are left alone.

**Expected output:**

```
add: ['approve-leave', 'read-reports']
remove: ['push-code', 'read-logs']
```
