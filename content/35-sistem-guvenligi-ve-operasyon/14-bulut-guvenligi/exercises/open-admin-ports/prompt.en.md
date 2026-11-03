Each network rule has `port` and `source`. `open_admin_ports(rules,
admin_ports)` should return, **once each** and from smallest to largest,
the ports of rules whose source is the whole internet (`"0.0.0.0/0"` or
`"::/0"`) and whose port is in `admin_ports`.

**Expected output:**

```
[22, 3389]
```
