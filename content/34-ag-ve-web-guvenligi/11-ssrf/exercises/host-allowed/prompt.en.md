`allowed(url, hosts)` should parse the address with `urlsplit` and
return `True` if its scheme is `http` or `https` **and** its host is
exactly in the `hosts` list, and `False` otherwise. The starter code checks
with a text search and is fooled by an address containing `@`.

**Expected output:**

```
True
False
False
False
```
