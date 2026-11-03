`policy` is an allow list where each item is `[src_zone, dst_zone,
port]`; `port` can be `"any"`. `allowed(flow, policy)` should return
`True` if the flow (`[src_zone, dst_zone, port]`) fits a line in the list,
and `False` otherwise (deny by default).

**Expected output:**

```
internet dmz 443 True
internet servers 5432 False
admin servers 22 True
dmz servers 22 False
```
