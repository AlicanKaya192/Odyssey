## Temel

| Yazım | Ne yapar |
|---|---|
| `async def f(): ...` | eş yordam fonksiyonu |
| `await f()` | çalıştır ve bekle (yalnızca `async def` içinde) |
| `asyncio.run(main())` | olay döngüsünü kur, çalıştır, kapat |
| `await asyncio.sleep(s)` | beklerken döngüyü serbest bırak |

## Birlikte çalıştırmak

| Yazım | Ne yapar |
|---|---|
| `await asyncio.gather(a(), b())` | hepsini bekle; sonuçlar verilen sırayla |
| `gather(..., return_exceptions=True)` | hatayı sonucun yerine koy |
| `task = asyncio.create_task(f())` | hemen başlat |
| `async with asyncio.TaskGroup() as g:` | görev grubu; biri düşerse diğerleri iptal |
| `except* ValueError as eg:` | `ExceptionGroup` içinden yakala |
| `for c in asyncio.as_completed(liste):` | biten önce |

## Sınırlar

| Yazım | Ne yapar |
|---|---|
| `async with asyncio.timeout(1):` | süre sınırı, dolunca `TimeoutError` |
| `await asyncio.wait_for(f(), timeout=1)` | tek iş için süre sınırı |
| `asyncio.Semaphore(3)` + `async with` | aynı anda en fazla 3 |
| `await asyncio.to_thread(f, x)` | engelleyen fonksiyonu iş parçacığında çalıştır |
| `asyncio.Queue()`; `await q.get()` | async kuyruk |

## Hatalar

| Belirti | Sebep |
|---|---|
| `RuntimeWarning: coroutine ... was never awaited` | `await` unutuldu |
| `gather` var ama süre toplamı kadar | `async def` içinde `time.sleep` ya da senkron G/Ç |
| `SyntaxError: 'await' outside async function` | `await` sıradan fonksiyonda |
| `RuntimeError: asyncio.run() cannot be called from a running event loop` | `asyncio.run` zaten çalışan döngünün içinden çağrıldı (Jupyter'de doğrudan `await main()`) |
