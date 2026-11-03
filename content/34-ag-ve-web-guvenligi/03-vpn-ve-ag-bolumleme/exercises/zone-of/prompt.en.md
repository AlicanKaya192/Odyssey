`zones` is a list where each item is `[name, cidr]`, and the networks
can be nested. `zone_of(ip_text, zones)` should return the name of the
network with the **largest prefix length** (the most specific) among those
that contain the address; `"unknown"` if none does. A network's prefix
length is `net.prefixlen`. The starter code returns the first match.

**Expected output:**

```
10.20.5.9 db
10.20.9.9 servers
10.1.1.1 corp
192.168.1.1 unknown
```
