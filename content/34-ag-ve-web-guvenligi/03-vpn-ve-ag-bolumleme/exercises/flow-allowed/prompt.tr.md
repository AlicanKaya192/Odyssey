`policy` her biri `[src_zone, dst_zone, port]` olan bir izin listesi;
`port` `"any"` olabilir. `allowed(flow, policy)` akış (`[src_zone,
dst_zone, port]`) listedeki bir satıra uyuyorsa `True`, değilse `False`
döndürsün (varsayılan reddet).

**Beklenen çıktı:**

```
internet dmz 443 True
internet servers 5432 False
admin servers 22 True
dmz servers 22 False
```
