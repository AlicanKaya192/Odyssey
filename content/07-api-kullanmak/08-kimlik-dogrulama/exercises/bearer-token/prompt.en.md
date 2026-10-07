The `/me` endpoint says which user signed in with the token. The token:
`letmein`.

**What to do:**

1. Send the token **without the prefix** (`Authorization: letmein`) and print
   the status code; you will see why it fails.
2. Send it in the right form (`Authorization: Bearer letmein`); print the
   status code, the user and the role.

**Expected output:**

```
no prefix: 401
with Bearer: 200
user: ada
role: editor
```
