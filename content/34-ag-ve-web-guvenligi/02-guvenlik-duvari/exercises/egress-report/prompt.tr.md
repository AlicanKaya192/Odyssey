`connections` içeriden dışarıya `[host, port]` denemeleri, `allowed` izin
verilen portlar. `blocked(connections, allowed)` engellenen denemeleri
`"host:port"` metinleri olarak döndürsün: ilk görüldükleri sırayla ve
**tekrarsız**.

**Beklenen çıktı:**

```
192.168.1.10:8888
192.168.1.30:2525
```
