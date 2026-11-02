In the matrix, the key `"*"` in a subject's row means **every object**.
For example `{"*": ["read"], "grades": ["write"]}` can read everything and
can also write to `grades`.

`effective_actions(matrix, subject, obj)` should return the actions the
subject may do on that object, as the union of the `obj` entry and the
`"*"` entry, as a list **without repeats and in alphabetical order**. An
empty list for an unknown subject or object.

**Expected output:**

```
['read', 'write']
['read']
[]
[]
```
