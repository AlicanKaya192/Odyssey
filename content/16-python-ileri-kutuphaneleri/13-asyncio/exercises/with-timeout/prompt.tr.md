`fetch_or_default(delay, limit)` `slow(delay)`'i en fazla `limit` saniye
beklesin: zamanında biterse sonucunu (`"ok"`), süre dolarsa `"timeout"`
metnini döndürsün. `async with asyncio.timeout(limit):` ve
`except TimeoutError` kullan. `check` sarmalayıcısını değiştirme.

**Beklenen çıktı:**

```
ok timeout
```
