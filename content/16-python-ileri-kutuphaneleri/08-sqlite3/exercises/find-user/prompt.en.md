The starter's `find_user(name)` builds the query with an f-string: given
`x' OR '1'='1`, every user comes back. Rewrite the function with the `?`
placeholder; return the names of the users whose name matches exactly, as a
list.

**Expected output:**

```
['ada']
[]
```
