Havuz (`ThreadPoolExecutor`) işlerin hepsi baştan belliyken kolay. İşler
**zamanla geliyorsa** (bir dosya okundukça, kullanıcı tıkladıkça) klasik
düzen **üretici–tüketici**: işler bir kuyruğa konur, işçiler kuyruktan alıp
işler. `queue.Queue` iş parçacıkları arasında güvenlidir; kendi kilidi var.

```python
import queue
import threading

tasks = queue.Queue()
results = queue.Queue()
STOP = None


def worker():
    while True:
        item = tasks.get()
        if item is STOP:
            break
        results.put((item, item * item))


workers = [threading.Thread(target=worker) for _ in range(3)]
for w in workers:
    w.start()
for n in range(10):
    tasks.put(n)
for _ in workers:
    tasks.put(STOP)
for w in workers:
    w.join()
collected = sorted(results.get() for _ in range(results.qsize()))
print(len(collected), collected[:3], collected[-1])
```

```text
10 [(0, 0), (1, 1), (2, 4)] (9, 81)
```

## Parçalar

- **`tasks.put(iş)`** kuyruğa ekler; **`tasks.get()`** bir iş alır, kuyruk
  boşsa **bekler** (işçi boşuna dönmez).
- **Durdurma işareti** (`STOP = None`): her işçiye bir tane. İşçi işareti
  görünce döngüden çıkar. İşaret konmazsa işçiler sonsuza kadar `get()`'te
  bekler ve `join()` hiç dönmez.
- Sonuçlar da bir kuyrukta toplanıyor; birden çok iş parçacığının aynı
  listeye yazması yerine güvenli yol.
- Sonuçların sırası işçilerin hızına bağlı; bu yüzden sonda sıralandı.

## Ne zaman kuyruk, ne zaman havuz?

| Durum | Seçim |
|---|---|
| İşlerin listesi baştan belli | `ThreadPoolExecutor.map` |
| İşler zamanla geliyor, sınırlı sayıda işçi | `queue.Queue` + işçiler |
| Üretici tüketiciden hızlı, bellek dolmasın | `queue.Queue(maxsize=100)`: dolunca `put` bekler |
