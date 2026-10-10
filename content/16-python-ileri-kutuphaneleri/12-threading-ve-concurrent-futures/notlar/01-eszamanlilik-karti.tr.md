## concurrent.futures

| Yazım | Ne yapar |
|---|---|
| `with ThreadPoolExecutor(max_workers=8) as pool:` | iş parçacığı havuzu |
| `pool.map(f, girdiler)` | sonuçlar girdi sırasıyla |
| `future = pool.submit(f, x)` | tek iş, Future döner |
| `future.result(timeout=5)` | sonucu bekle; işteki hata burada yükselir |
| `as_completed(futures)` | biten önce gelir |
| `wait(futures, timeout=1)` | `(done, not_done)` kümeleri |
| `ProcessPoolExecutor` | süreç havuzu (CPU işi) |

## threading

| Yazım | Ne yapar |
|---|---|
| `t = threading.Thread(target=f, args=(x,))` | iş parçacığı tanımla |
| `t.start()`, `t.join()` | başlat, bekle |
| `lock = threading.Lock()` + `with lock:` | aynı anda tek iş parçacığı |
| `threading.active_count()` | çalışan iş parçacığı sayısı |
| `queue.Queue()`; `put`, `get` | güvenli kuyruk |

## Seçim

| İş | Araç |
|---|---|
| Ağ, disk, veritabanı beklemesi | `ThreadPoolExecutor` |
| Saf Python hesabı | `ProcessPoolExecutor` + `if __name__ == "__main__":` |
| Binlerce eşzamanlı bağlantı | `asyncio` |

## Tuzaklar

- Paylaşılan veriyi kilitsiz değiştirmek: artışlar kaybolur.
- `future.result()`'ı hiç çağırmamak: işteki hata görünmez kalır.
- Süreç havuzunu `if __name__ == "__main__":` olmadan açmak.
- Kuyruk işçilerine durdurma işareti koymamak: `join()` asılı kalır.
