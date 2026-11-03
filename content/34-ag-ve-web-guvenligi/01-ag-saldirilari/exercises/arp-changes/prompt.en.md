`replies` is a list of ARP answers, each `[ip, mac]` (in order of
arrival). `arp_changes(replies)` should keep a table; if a **different**
MAC was seen before for an address, it should add the list `[ip, old,
new]` to the result. The same MAC arriving again is not a change.

**Expected output:**

```
192.168.1.1
  old 02:00:00:00:00:fe
  new 02:00:00:00:00:66
```
