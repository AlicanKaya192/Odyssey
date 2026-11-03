`WELL_KNOWN` sözlüğü hazır. `service_for(port)` port 0 ile 65535
arasında değilse `"invalid"`, sözlükte varsa servisin adını, yoksa
`"unknown"` döndürsün.

**Beklenen çıktı:**

```
443 https
22 ssh
8081 unknown
70000 invalid
-1 invalid
```
