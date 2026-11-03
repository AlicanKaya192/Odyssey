`port_ok(url)` should return `True` if the address's real port is 80
or 443. If no port is written, the scheme's default is used (`http` → 80,
`https` → 443); any other scheme is `False`. `urlsplit(url).port` raises
`ValueError` on an invalid port: `False` in that case too.

**Expected output:**

```
True
False
True
False
False
```
