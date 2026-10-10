İş parçacıklarındaki üretici–tüketici düzeninin async karşılığı
**`asyncio.Queue`**. Bu sefer işçileri durdurma işaretiyle değil, iş bitince
**iptal ederek** kapatıyoruz.

```python
import asyncio


async def worker(queue, results):
    while True:
        n = await queue.get()
        await asyncio.sleep(0.01)
        results.append((n, n * n))
        queue.task_done()


async def main():
    queue = asyncio.Queue()
    results = []
    workers = [asyncio.create_task(worker(queue, results)) for _ in range(3)]
    for n in range(10):
        queue.put_nowait(n)
    await queue.join()
    for w in workers:
        w.cancel()
    await asyncio.gather(*workers, return_exceptions=True)
    print(len(results), sorted(results)[:3])


asyncio.run(main())
```

```text
10 [(0, 0), (1, 1), (2, 4)]
```

## Parçalar

- **`await queue.get()`** iş gelene kadar bekler; beklerken döngü başka
  görevleri çalıştırır.
- **`queue.task_done()`** "aldığım işi bitirdim" der. **`await queue.join()`**
  kuyruğa konan her iş için `task_done` gelene kadar bekler: yani bütün
  işler bitti.
- İşçiler hâlâ `get()`'te bekliyor; **`cancel()`** onlara iptal gönderir.
  `gather(..., return_exceptions=True)` iptallerin bitmesini bekler ve
  `CancelledError`'ları yutar.
- `results` sıradan bir liste: tek iş parçacığında çalıştığımız için
  kilit gerekmiyor. Görevler yalnızca `await` noktalarında yer değiştiriyor;
  `results.append` bölünmüyor.

## İş parçacığı kuyruğu ile farkı

| | `queue.Queue` | `asyncio.Queue` |
|---|---|---|
| Kimler arasında | iş parçacıkları | aynı döngüdeki görevler |
| Beklemek | `q.get()` (iş parçacığını durdurur) | `await q.get()` (döngü devam eder) |
| Kilit | kendi içinde var | gerekmez |
| Durdurmak | işaret (`STOP`) | `join()` + `cancel()` ya da işaret |
