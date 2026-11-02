`to_acl(matrix)` should turn the matrix into an access list object by
object: the key is the object, the value is the **alphabetical** list of
`"subject:action"` texts. An object with no permission at all should not
appear in the dictionary.

Example: `{"ada": {"grades": ["read", "write"]}}` →
`{"grades": ["ada:read", "ada:write"]}`.

**Expected output:**

```
grades ada:read, ada:write, alan:read
payroll alan:read
```
