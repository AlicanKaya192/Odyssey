`download_all(count, limit)` `count` indirmeyi `gather` ile birlikte başlatıyor
ve `[indirme sayısı, aynı anda çalışan en çok indirme]` döndürüyor. Şu an
hepsi aynı anda çalışıyor. `download_all` içinde `asyncio.Semaphore(limit)`
kur ve `download` içindeki işi `async with gate:` bloğuna al; tepe değer
`limit`'i geçmesin.

**Beklenen çıktı:**

```
[10, 3]
```
