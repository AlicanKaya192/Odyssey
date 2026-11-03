`is_internal(text)` should take an IP address text and return `True`
if the address is private, loopback, link-local, unspecified or reserved,
and `False` otherwise. If the text is not a valid IP address, also return
`True`: refuse when unsure (`ipaddress.ip_address` raises
`ValueError`).

**Expected output:**

```
100.20.30.40 False
127.0.0.1 True
10.1.2.3 True
169.254.169.254 True
0.0.0.0 True
not-an-ip True
```
