# asyncio

Önceki bölümde beklemeleri iş parçacıklarıyla üst üste bindirdin. **asyncio**
aynı işi tek bir iş parçacığında yapar: her fonksiyon beklemeye geçtiği anda
"ben bekliyorum, sen devam et" der ve sıra bir sonrakine geçer. Binlerce ağ
bağlantısını aynı anda idare eden sunucular (FastAPI, aiohttp) bu modelle
çalışır. Bu bölüm `async` / `await` yazımını, işleri birlikte çalıştırmayı,
süre sınırını, hataları ve en sık yapılan hatayı (beklerken engellemek)
anlatıyor.

## async def, await, asyncio.run

```python
import asyncio


async def fetch(n):
    await asyncio.sleep(0.2)
    return n * n


async def main():
    pending = fetch(2)
    print(type(pending).__name__)
    print(await pending)


asyncio.run(main())
```

```text
coroutine
4
```

- **`async def`** bir **eş yordam** (coroutine) fonksiyonu tanımlar.
  Çağırmak onu çalıştırmaz; bir `coroutine` nesnesi döndürür (ilk satır).
- **`await`** eş yordamı çalıştırır ve sonucunu bekler. `await` yalnızca
  başka bir `async def`'in içinde yazılabilir.
- **`await asyncio.sleep(0.2)`** "0,2 saniye bekleyeceğim, bu arada başka
  işler çalışsın" demek. `time.sleep` bunu demez (aşağıda).
- **`asyncio.run(main())`** olay döngüsünü (event loop) kurar, `main`'i
  sonuna kadar çalıştırır ve kapatır. Programda genellikle bir kez, en dışta
  çağrılır.

## gather: birlikte beklemek

```python
import asyncio
import time


async def fetch(n):
    await asyncio.sleep(0.2)
    return n * n


async def main():
    start = time.perf_counter()
    one_by_one = [await fetch(n) for n in range(5)]
    sequential = time.perf_counter() - start
    start = time.perf_counter()
    together = await asyncio.gather(*(fetch(n) for n in range(5)))
    concurrent = time.perf_counter() - start
    print(one_by_one, together)
    print(sequential >= 1.0, concurrent < 0.5)


asyncio.run(main())
```

```text
[0, 1, 4, 9, 16] [0, 1, 4, 9, 16]
True True
```

- `await` ile sırayla çağırmak beklemeleri toplar: 5 × 0,2 = 1 saniye.
- **`asyncio.gather(eş yordamlar...)`** hepsini birlikte başlatır, hepsi
  bitince sonuçları **verilen sırayla** liste olarak döndürür. Bu
  bilgisayarda 0,2 saniye.
- Tek iş parçacığı var; hız, bekleme sırasında başka eş yordama geçilmesinden
  geliyor.

## En sık hata: beklerken engellemek

```python
import asyncio
import time


async def blocking(n):
    time.sleep(0.2)
    return n


async def main():
    start = time.perf_counter()
    await asyncio.gather(*(blocking(n) for n in range(3)))
    blocked = time.perf_counter() - start
    start = time.perf_counter()
    await asyncio.gather(*(asyncio.to_thread(time.sleep, 0.2) for _ in range(3)))
    offloaded = time.perf_counter() - start
    print(blocked >= 0.6, offloaded < 0.4)


asyncio.run(main())
```

```text
True True
```

- **`time.sleep`** olay döngüsünü **durdurur**: o sırada hiçbir eş yordam
  çalışamaz. `gather` kullanılmasına rağmen üç iş sırayla gitti (0,6 sn).
  Aynısı `requests.get`, büyük bir dosyayı okumak, uzun bir hesap için de
  geçerli.
- `async def` içinde yalnızca **`await` edilebilen** beklemeler kullanılır:
  `asyncio.sleep`, async kütüphaneler (`aiohttp`, `httpx`'in async istemcisi,
  async veritabanı sürücüleri).
- Engelleyen bir fonksiyonu mecburen çağıracaksan **`asyncio.to_thread(f,
  ...)`** onu ayrı bir iş parçacığında çalıştırır ve döngü serbest kalır
  (0,2 sn).

## Süre sınırı: timeout

```python
import asyncio


async def slow():
    await asyncio.sleep(1)
    return "done"


async def main():
    try:
        async with asyncio.timeout(0.1):
            await slow()
    except TimeoutError:
        print("TimeoutError")
    try:
        await asyncio.wait_for(slow(), timeout=0.1)
    except TimeoutError:
        print("wait_for: TimeoutError")


asyncio.run(main())
```

```text
TimeoutError
wait_for: TimeoutError
```

- **`async with asyncio.timeout(saniye):`** bloğun içindeki her şeye süre
  sınırı koyar; süre dolunca içerideki iş **iptal edilir** ve
  `TimeoutError` yükselir.
- **`asyncio.wait_for(eş yordam, timeout=...)`** tek bir iş için aynısı.
- Ağdan veri bekleyen her işe süre sınırı konur; cevap vermeyen bir sunucu
  programı sonsuza kadar bekletmesin.

## Görevler ve hatalar: TaskGroup

```python
import asyncio


async def job(name, delay, fail=False):
    await asyncio.sleep(delay)
    if fail:
        raise ValueError(name)
    return name


async def main():
    async with asyncio.TaskGroup() as group:
        a = group.create_task(job("a", 0.2))
        b = group.create_task(job("b", 0.1))
    print(a.result(), b.result())
    try:
        async with asyncio.TaskGroup() as group:
            group.create_task(job("x", 0.1, fail=True))
            y = group.create_task(job("y", 0.5))
    except* ValueError as errors:
        print([str(e) for e in errors.exceptions], y.cancelled())
    results = await asyncio.gather(job("p", 0.1), job("q", 0.05, fail=True),
                                   return_exceptions=True)
    print(results)


asyncio.run(main())
```

```text
a b
['x'] True
['p', ValueError('q')]
```

- **`create_task`** bir eş yordamı **görev** (task) olarak hemen başlatır.
- **`asyncio.TaskGroup`** bir görev grubu: `async with` bloğu bitince
  gruptaki bütün görevlerin bitmesi beklenir. Sonuçlar `task.result()` ile.
- Gruptaki bir görev hata verirse **diğerleri iptal edilir** (`y` bitmeden
  iptal oldu) ve hatalar bir `ExceptionGroup` içinde toplanır.
  **`except*`** bu gruptaki belirli türdeki hataları yakalar.
- **`gather(..., return_exceptions=True)`** hatayı yükseltmek yerine sonucun
  yerine koyar: biri düşse de diğerleri tamamlanır.

## Aynı anda kaç tane? Semaphore

```python
import asyncio


async def download(n, gate, state):
    async with gate:
        state["active"] += 1
        state["peak"] = max(state["peak"], state["active"])
        await asyncio.sleep(0.05)
        state["active"] -= 1
        return n


async def main():
    gate = asyncio.Semaphore(3)
    state = {"active": 0, "peak": 0}
    results = await asyncio.gather(*(download(n, gate, state) for n in range(10)))
    print(len(results), state["peak"])


asyncio.run(main())
```

```text
10 3
```

- On görev aynı anda başladı ama **`asyncio.Semaphore(3)`** kapısından aynı
  anda en fazla üçü geçebildi (`peak` 3).
- Bir sunucuya aynı anda bin istek atmak onu (ve seni) zorlar; çoğu API
  eşzamanlı istek sayısını sınırlar. Semaphore bu sınırı kodda tutar.

## Ne zaman asyncio?

| Durum | Seçim |
|---|---|
| Çok sayıda ağ beklemesi, async kütüphane var | `asyncio` |
| Birkaç bekleme, kütüphane senkron (`requests`) | `ThreadPoolExecutor` |
| İşlemci yoğun hesap | `ProcessPoolExecutor` |
| Async kodun içinde engelleyen bir çağrı | `asyncio.to_thread` |

## Özet

- `async def` eş yordam tanımlar; `await` çalıştırıp bekler; en dışta
  `asyncio.run(main())`.
- `gather` birlikte bekler, sonuçlar verilen sırayla.
- `async def` içinde `time.sleep` ve senkron G/Ç yok; gerekirse `to_thread`.
- `asyncio.timeout` / `wait_for` ile süre sınırı.
- `TaskGroup`: biri düşerse diğerleri iptal; `except*` ile yakala.
- `Semaphore(n)` eşzamanlı iş sayısını sınırlar.
