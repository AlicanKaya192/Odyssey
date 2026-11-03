`is_internal_ip(ip)` is ready. `safe_target(url, dns)` should find the
address's host (`urlsplit`) and read its entry in the `dns` dictionary as
an IP if there is one, otherwise the name itself. If there is no host or
the IP cannot be read, return `"unknown host"`; if the IP is internal,
`"blocked"`; otherwise `"ok"`. The starter code looks only at the name.

**Expected output:**

```
ok
blocked
blocked
unknown host
unknown host
```
