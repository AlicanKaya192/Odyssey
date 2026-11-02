Combine the Authorization and Access Control Models sections.

`can_access(user, action, doc, user_roles, role_perms)`:

1. `True` if one of the user's roles contains the action.
2. Otherwise `True` if the user owns the document (`doc["owner"]`) and the
   action is `"read"` or `"edit"`.
3. Everything else is `False`, including an unknown user and an unknown
   role.

**Expected output:**

```
ada edit True
bora edit False
ceren edit True
ceren delete False
zeynep read False
```
