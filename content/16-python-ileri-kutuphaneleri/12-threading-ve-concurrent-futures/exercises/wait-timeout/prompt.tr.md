`finished_within(delays, limit)` her gecikme için `pool.submit(nap, d)`
yapsın ve `concurrent.futures.wait(futures, timeout=limit)` ile en fazla
`limit` saniye beklesin. `[biten iş sayısı, bitmeyen iş sayısı]` listesini
döndürsün. Başlangıç kodu bütün işleri sonuna kadar bekliyor.

**Beklenen çıktı:**

```
[2, 1]
```
