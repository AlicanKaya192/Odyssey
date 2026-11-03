If a packet coming from outside has a source in the internal network
or a loopback address, the packet is forged. `ingress_ok(src, internal)`
should return `False` in that case and `True` otherwise. `internal` is the
internal network in CIDR form (`"192.168.1.0/24"`). The starter code
forgets loopback.

**Expected output:**

```
203.0.113.7 True
192.168.1.20 False
127.0.0.1 False
```
