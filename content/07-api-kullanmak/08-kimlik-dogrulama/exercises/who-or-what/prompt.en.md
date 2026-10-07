`/admin/report` can cause two different problems: `401` if the key is wrong,
`403` if it is valid but not allowed. You will write a function that says
which one it is.

**What to do:**

1. Write the function `access(key)`: it sends a request to `/admin/report`
   with the `X-API-Key` header and returns
   - `"ok"` on `200`,
   - `"unknown key"` on `401`,
   - `"not allowed"` on `403`.
2. For every key in the `keys` list, print the key and the result.

**Expected output:**

```
admin-key-999 -> ok
demo-key-123 -> not allowed
my-guess -> unknown key
```
