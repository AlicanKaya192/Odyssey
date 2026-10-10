# threading ve concurrent.futures

Bir program çoğu zaman **bekler**: ağdan cevap, diskten dosya, veritabanından
sonuç. Beş isteği sırayla atıp her birini beklemek, beklemelerin toplamı kadar
sürer. **İş parçacıkları** (thread) beklerken başka işe geçmeyi sağlar. Bu
bölüm `threading` ve onun üstündeki kolay arayüz `concurrent.futures`'ı
anlatıyor: ne zaman hızlandırır, ne zaman hızlandırmaz, ve paylaşılan veride
neyin bozulabileceği.

## Beklerken başka iş: ThreadPoolExecutor

```python
import time
from concurrent.futures import ThreadPoolExecutor


def fetch(n):
    time.sleep(0.2)
    return n * n


start = time.perf_counter()
one_by_one = [fetch(n) for n in range(5)]
sequential = time.perf_counter() - start

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as pool:
    together = list(pool.map(fetch, range(5)))
threaded = time.perf_counter() - start

print(one_by_one, together)
print(sequential >= 1.0, threaded < 0.5)
```

```text
[0, 1, 4, 9, 16] [0, 1, 4, 9, 16]
True True
```

- `fetch` ağdan veri bekleyen bir fonksiyonu taklit ediyor: 0,2 saniye uyuyor.
  Beş tanesi sırayla 1 saniye sürüyor; bu bilgisayarda havuzla
  yaklaşık 0,2 saniye.
- **`ThreadPoolExecutor(max_workers=5)`** beş iş parçacığından bir **havuz**
  kurar. `pool.map(fonksiyon, girdiler)` her girdiyi boştaki bir iş
  parçacığına verir; sonuçlar **girdi sırasıyla** gelir.
- `with` bloğu bitince havuz bütün işlerin bitmesini bekler ve kapanır.
- İşe yarıyor çünkü uyuyan (bekleyen) iş parçacığı işlemciyi bırakıyor;
  ağ, disk, veritabanı beklemesi böyledir.

## Thread nesnesi: elle başlatıp beklemek

```python
import threading

results = {}


def work(name, n):
    results[name] = sum(range(n))


threads = []
for i in range(1, 4):
    threads.append(threading.Thread(target=work, args=(f"t{i}", 10 ** i)))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print(sorted(results.items()))
print(threading.active_count())
```

```text
[('t1', 45), ('t2', 4950), ('t3', 499500)]
1
```

- **`Thread(target=fonksiyon, args=(...))`** bir iş parçacığı tanımlar,
  **`start()`** çalıştırır, **`join()`** bitmesini bekler.
- İş parçacığı bir değer **döndüremez**; sonuç paylaşılan bir yapıya
  (burada sözlük) yazılır. Havuzun `map`/`submit`'i bu işi senin yerine
  yaptığı için çoğu zaman tercih edilir.
- Hepsi `join` edilince yalnızca ana iş parçacığı kalır: `active_count()` 1.

## Yarış durumu (race condition) ve Lock

```python
import threading
import time

count = 0


def add():
    global count
    for _ in range(1000):
        value = count
        time.sleep(0)
        count = value + 1


workers = [threading.Thread(target=add) for _ in range(4)]
for w in workers:
    w.start()
for w in workers:
    w.join()
print(count < 4000)

count = 0
lock = threading.Lock()


def safe_add():
    global count
    for _ in range(1000):
        with lock:
            value = count
            time.sleep(0)
            count = value + 1


workers = [threading.Thread(target=safe_add) for _ in range(4)]
for w in workers:
    w.start()
for w in workers:
    w.join()
print(count)
```

```text
True
4000
```

- Dört iş parçacığı 1000'er kez artırıyor; 4000 beklenir. Ama "oku, sonra
  yaz" arasında başka bir iş parçacığı araya girerse (burada `sleep(0)` bunu
  kolaylaştırıyor) ikisi aynı eski değeri okuyup aynı yeni değeri yazıyor:
  artışlar **kayboluyor**. Bu bilgisayarda sonuç her çalıştırmada farklıydı
  (1047 ile 1622 arası).
- **`threading.Lock`** bir kilit: `with lock:` bloğuna aynı anda yalnızca bir
  iş parçacığı girer. Oku-değiştir-yaz işlemi bölünmez hâle gelir; sonuç
  4000.
- Kural: birden çok iş parçacığının **değiştirdiği** her paylaşılan veri
  kilitle korunur. Yalnızca okunan veri ve havuzun döndürdüğü sonuçlar
  sorun değil.
- `count += 1` gibi tek satır da güvenli değildir: perde arkasında yine
  oku-topla-yaz. Bu bilgisayarda kilitsiz `+=` hata göstermedi, ama Python
  bunu garanti etmiyor; ileride çıkacak hatayı bulmak çok zordur.

## Future: işin sözü

```python
from concurrent.futures import ThreadPoolExecutor, as_completed


def check(x):
    if x < 0:
        raise ValueError(f"negative: {x}")
    return x * 10


with ThreadPoolExecutor() as pool:
    futures = {pool.submit(check, x): x for x in [1, -2, 3]}
    done = []
    for future in as_completed(futures):
        x = futures[future]
        try:
            done.append((x, future.result()))
        except ValueError as error:
            done.append((x, f"error: {error}"))
print(sorted(done))
```

```text
[(-2, 'error: negative: -2'), (1, 10), (3, 30)]
```

- **`pool.submit(fonksiyon, argüman)`** işi hemen kuyruğa koyar ve bir
  **Future** döndürür: "sonuç ileride burada olacak" sözü.
- **`future.result()`** sonucu bekler ve verir. İş içinde hata çıktıysa
  hata **burada**, `result()` çağrılınca yükselir; yakalamazsan kaybolmaz.
- **`as_completed(futures)`** işleri **bitiş sırasıyla** verir; ilk biten
  ilk gelir. Sıra her çalıştırmada değişebileceği için sonuç sonda
  sıralandı.
- Sözlükte Future → girdi eşlemesi tutmak, hangi sonucun hangi girdiye ait
  olduğunu bilmenin yaygın yolu.

## İşlemci yoğun iş: GIL ve ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def cpu(n):
    total = 0
    for i in range(n):
        total += i * i
    return total


if __name__ == "__main__":
    jobs = [300_000] * 4
    plain = [cpu(n) for n in jobs]
    with ThreadPoolExecutor(max_workers=4) as pool:
        threaded = list(pool.map(cpu, jobs))
    with ProcessPoolExecutor(max_workers=4) as pool:
        processed = list(pool.map(cpu, jobs))
    print(plain == threaded == processed, plain[0])
```

```text
True 8999955000050000
```

- Standart Python'da (CPython) bir **GIL** (global interpreter lock) var:
  aynı anda yalnızca bir iş parçacığı Python kodu çalıştırır. Bekleyen iş
  parçacığı kilidi bırakır, o yüzden G/Ç işlerinde havuz hızlandırıyor;
  ama hesap yapan döngülerde iş parçacıkları sırayla çalışır.
- Aynı kod `jobs = [3_000_000] * 4` ile ve süre ölçülerek çalıştırılınca bu
  bilgisayarda: sırayla 0,63 sn, iş parçacıklarıyla yine 0,63 sn, **süreç
  havuzuyla 0,39 sn**.
- **`ProcessPoolExecutor`** ayrı Python süreçleri açar; her birinin kendi
  GIL'i var, işler gerçekten aynı anda çalışır. Bedeli: süreç açmak zaman
  alır, girdiler ve sonuçlar pickle ile taşınır (pickle bölümü), küçük
  işlerde kazançtan çok kayıp olabilir.
- **`if __name__ == "__main__":`** şart: Windows'ta yeni süreç dosyayı
  baştan içe aktarır; koruma olmazsa her süreç yeni süreçler açmaya kalkar.
- Python 3.13'ten beri GIL'siz ("free-threaded") ayrı bir Python sürümü de
  var; orada iş parçacıkları hesapta da hızlanabilir. Bu bilgisayardaki
  Python GIL'li.

## Hangisi ne zaman?

| İş | Araç |
|---|---|
| Ağ, disk, veritabanı beklemesi (G/Ç) | `ThreadPoolExecutor` |
| Saf Python hesabı, büyük döngü (CPU) | `ProcessPoolExecutor` |
| NumPy / pandas hesabı | çoğu zaman gerekmez; kütüphane C'de çalışıyor |
| Binlerce eşzamanlı bağlantı | `asyncio` (sonraki bölüm) |

## Özet

- `ThreadPoolExecutor` + `map` / `submit`: beklemeleri üst üste bindirir.
- `Thread(target=..., args=...)`, `start()`, `join()`; sonuç paylaşılan yapıya.
- Paylaşılan veriyi değiştiren her yer `with lock:`.
- Future: `result()` sonucu verir ya da işteki hatayı yükseltir;
  `as_completed` bitiş sırası.
- CPU işi için süreç havuzu ve `if __name__ == "__main__":`.
