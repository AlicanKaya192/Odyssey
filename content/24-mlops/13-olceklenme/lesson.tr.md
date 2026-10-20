# Ölçeklenme

Model Sunma bölümünde tek bir sunucu kurduk. Müşteri sayısı büyüyünce
sorular değişir: bir sunucu kaç isteğe yetişir, dolmaya yaklaşınca ne
olur, aynı soruyu tekrar tekrar hesaplamak gerekir mi, daha büyük model
buna değer mi? **Ölçeklenme** (scaling), yük büyürken hizmetin hızlı ve
ucuz kalmasıdır. Bu bölümde dört soruyu ölçerek cevaplıyoruz.

## Toplu mu, anlık mı?

İlk soru tahminin **ne zaman** hesaplanacağıdır:

| | Toplu tahmin (batch) | Anlık tahmin (online) |
|---|---|---|
| Ne zaman | Önceden, örneğin her gece bütün müşteriler için | İstek geldiği anda |
| Sonuç nerede | Bir tabloda; uygulama oradan okur | Sunucunun cevabında |
| Artısı | Ucuz, basit, hız sorunu yok | Taze bilgiyle hesaplar |
| Eksisi | Bilgi bir gün eski olabilir | Sunucu ayakta ve hızlı olmalı |

Model Sunma bölümünde toplu çağrının müşteri başına en az on kat hızlı
olduğunu ölçmüştük. İptal riski gibi günde bir değişen bir skor için
çoğu zaman toplu tahmin yeter; anlık tahmin, cevabın o anki bilgiye
(sepetteki ürün, son tıklama) bağlı olduğu yerde gerekir.

## Doluluk ve bekleme

Anlık tahminde istekler rastgele anlarda gelir. Bir sunucunun **doluluğu**
(utilization), zamanının ne kadarında meşgul olduğudur: saniyede 50 istek
gelir ve her biri 10 ms sürerse sunucu zamanın yarısında meşguldür (%50).
Doluluk büyüdükçe ne olur? Küçük bir benzetimle ölçelim: istekler rastgele
gelir, her biri ortalama 10 ms sürer, sunucu boşsa hemen başlar, doluysa
istek sırada bekler.

```python
import heapq
import random


def simulate(load, workers, n=20000, seed=1):
    rng = random.Random(seed)
    service = 10.0
    gap = service / (load * workers)
    free = [0.0] * workers
    now, waits = 0.0, []
    for _ in range(n):
        now += rng.expovariate(1 / gap)
        start = max(now, free[0])
        waits.append(start - now)
        heapq.heapreplace(free, start + rng.expovariate(1 / service))
    waits.sort()
    return round(sum(waits) / n, 1), round(waits[int(0.95 * n)], 1)


for load in [0.5, 0.8, 0.9, 0.95, 0.99]:
    mean, p95 = simulate(load, 1)
    print(f"load {load:.2f}: mean wait {mean:>6} ms  p95 {p95:>7} ms")
```

```text
load 0.50: mean wait    9.8 ms  p95    45.3 ms
load 0.80: mean wait   36.4 ms  p95   120.9 ms
load 0.90: mean wait   74.1 ms  p95   226.6 ms
load 0.95: mean wait  147.3 ms  p95   422.8 ms
load 0.99: mean wait  329.5 ms  p95  1131.2 ms
```

`rng.expovariate` rastgele ama ortalaması belli aralıklar üretir: istekler
düzenli değil, kümelenerek gelir. `free` her çalışanın ne zaman boşalacağını
tutan bir yığın (heap, Algoritmalar patikası): en erken boşalan hep
başta. `heapreplace` onu çıkarıp yenisini koyar.

Sonuç doğrusal değil. Doluluk %50'den %90'a çıkınca ortalama bekleme
9,8 ms'den 74,1 ms'ye çıkıyor; %99'da 329,5 ms. Her
istek hâlâ yalnızca 10 ms sürüyor; zamanın geri kalanı **sırada**
geçiyor. Sunucu "daha yüzde 10 boş yeri var" gibi görünürken aslında
yavaştır. Bu yüzden sunucular %100'e göre değil, örneğin %70 doluluğa
göre planlanır.

Aynı doluluğu daha çok çalışana dağıtmak da fark eder:

```python
for workers in [1, 2, 4]:
    mean, p95 = simulate(0.9, workers)
    print(f"workers={workers} at 90%: mean wait {mean:>5} ms  p95 {p95:>6} ms")
```

```text
workers=1 at 90%: mean wait  74.1 ms  p95  226.6 ms
workers=2 at 90%: mean wait  34.5 ms  p95  110.6 ms
workers=4 at 90%: mean wait  15.4 ms  p95   52.8 ms
```

Dört çalışan da %90 dolu; ama ortak bir sırayı paylaştıkları için biri
boşalınca bekleyen hemen ona gider. Bekleme 74,1 ms'den 15,4
ms'ye iniyor. Bu, **yatay ölçeklenmenin** (horizontal scaling: aynı
sunucudan birkaç tane) bir artısıdır. Bunun için sunucunun **durumsuz**
(stateless) olması gerekir: her istek, hangi kopyaya giderse gitsin aynı
cevabı alır. Model Sunma bölümündeki sunucu böyledir; model açılışta
yüklenir, istekler arasında bilgi saklanmaz.

## Önbellek

Aynı müşteri için gün içinde birçok istek gelebilir. Skor değişmediyse
her seferinde yeniden hesaplamak yerine son cevabı saklamak **önbellek**
(cache) fikridir. İstekler müşterilere eşit dağılmaz: birkaç müşteri çok,
çoğu az istek alır. Bunu ağırlıklı bir seçimle taklit edelim ve
belirli boyda bir önbellek ne kadarını karşılar ölçelim:

```python
from collections import OrderedDict

rng = random.Random(3)
customers = list(range(10000))
weights = [1 / (rank + 1) for rank in customers]
requests = rng.choices(customers, weights=weights, k=50000)
print(len(set(requests)), "different customers in", len(requests), "requests")


def hit_rate(size):
    cache, hits = OrderedDict(), 0
    for customer in requests:
        if customer in cache:
            hits += 1
            cache.move_to_end(customer)
        else:
            cache[customer] = True
            if len(cache) > size:
                cache.popitem(last=False)
    return round(hits / len(requests), 3)


for size in [10, 100, 1000, 5000]:
    print(f"cache {size:>4}: {hit_rate(size)} of requests answered from cache")
```

```text
6794 different customers in 50000 requests
cache   10: 0.128 of requests answered from cache
cache  100: 0.388 of requests answered from cache
cache 1000: 0.667 of requests answered from cache
cache 5000: 0.852 of requests answered from cache
```

Bu önbellek **LRU** (least recently used) türündedir: dolunca en uzun
süredir sorulmayanı çıkarır. `OrderedDict` sırayı tutar, `move_to_end`
yeni sorulanı sona alır, `popitem(last=False)` baştakini atar. Python'da
aynı fikrin hazır hâli `functools.lru_cache`.

Yalnızca 100 müşterilik yer isteklerin 0,388 kadarını
karşılıyor: çok sorulan az sayıda müşteri yükün büyük kısmını taşıyor.
Ama önbelleğin bir bedeli var: **bayatlık**. Saklanan skor, müşterinin
bilgisi değişince ya da model değişince eskir. Bu yüzden önbellekteki her
kaydın bir ömrü (TTL, time to live) olur ve anahtar yalnızca müşteri değil,
**müşteri + model sürümü**dür: yeni model canlıya alınınca eski skorlar
kendiliğinden kullanılmaz olur.

## Model ne kadar büyük olmalı?

Daha büyük model her istekte daha çok iş demektir. Bir rastgele ormanda
(random forest) her tahmin bütün ağaçlardan geçer. Ağaç sayısını
büyütelim:

```python
from sklearn.ensemble import RandomForestClassifier
from ml_data import make_customers, NUMERIC


def features(r):
    return [r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


train, test = make_customers(2000), make_customers(1000, seed=99)
X, y = [features(r) for r in train], [r["churned"] for r in train]
X_test, y_test = [features(r) for r in test], [r["churned"] for r in test]
for trees in [5, 20, 100, 400]:
    model = RandomForestClassifier(n_estimators=trees, max_depth=6, random_state=0)
    model.fit(X, y)
    print(f"{trees:>3} trees: accuracy {model.score(X_test, y_test):.3f}")
```

```text
  5 trees: accuracy 0.810
 20 trees: accuracy 0.812
100 trees: accuracy 0.813
400 trees: accuracy 0.814
```

Ağaç sayısı 80 katına çıkıyor, doğruluk yalnızca 0,004 artıyor.
Bu bilgisayarda tek müşterilik tahmin 5 ağaçla 1 ms dolayında, 400 ağaçla
onlarca kat uzun (yaklaşık 45 ms) sürüyor. Her istek onlarca kat uzarsa,
aynı doluluk için onlarca kat çok sunucu gerekir. Model seçimi yalnızca
doğrulukla yapılmaz; **gecikme ve maliyet** de ölçülür ve bir sınır
konur (örneğin "p95 50 ms'yi geçmesin").

## Özet

| Soru | Araç | Dersteki ölçüm |
|---|---|---|
| Ne zaman hesaplanmalı? | Toplu ya da anlık | Toplu çağrı müşteri başına en az on kat hızlı |
| Sunucu ne kadar dolu olmalı? | Doluluk planı | %50'de 9,8 ms, %99'da 329,5 ms bekleme |
| Çok sunucu ne kazandırır? | Yatay ölçeklenme | %90'da 1 çalışan 74,1 ms, 4 çalışan 15,4 ms |
| Aynı soru tekrar mı hesaplanmalı? | Önbellek (LRU) | 100 müşterilik yer isteklerin 0,388'i |
| Büyük model değer mi? | Gecikme ile doğruluk dengesi | 5 → 400 ağaç: 0,810 → 0,814 |

- Doluluk %100'e yaklaştıkça bekleme doğrusal değil, birden büyür;
  sunucular boşlukla planlanır.
- Yatay ölçeklenme için sunucu durumsuz olmalı.
- Önbellek anahtarı müşteri + model sürümü; kayıtların ömrü olur.
- Model seçiminde gecikme ve maliyet de ölçülür.
