With split tunneling, only traffic to certain networks goes through
the VPN. `route(dst, tunnel_networks)` should return `"vpn"` if the
destination address is in one of the networks in the list, and `"direct"`
otherwise.

**Expected output:**

```
10.20.0.15 vpn
172.20.1.1 vpn
203.0.113.7 direct
```
