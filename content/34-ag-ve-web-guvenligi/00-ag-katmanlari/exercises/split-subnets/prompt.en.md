`split(cidr, new_prefix)` should split the network into equal parts
with prefix `new_prefix` and return the parts as text
(`"192.168.1.0/26"`) in a list.
`ipaddress.ip_network(cidr).subnets(new_prefix=...)` gives the parts; turn
each into text with `str`.

**Expected output:**

```
192.168.1.0/26
192.168.1.64/26
192.168.1.128/26
192.168.1.192/26
256
```
