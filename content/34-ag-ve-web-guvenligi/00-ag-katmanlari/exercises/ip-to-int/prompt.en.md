`ip_to_int(text)` should turn a dotted IPv4 address (`"192.168.1.10"`)
into a single integer. Split the parts with `split(".")`; for each part,
multiply the value by 256 and add the part.

**Expected output:**

```
3232235786
167772161
4294967295
```
