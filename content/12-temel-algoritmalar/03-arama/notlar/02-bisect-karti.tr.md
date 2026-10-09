`bisect` modülü sıralı bir listede ikili aramanın hazır hâli. Liste
**sıralı olmalı**; değilse hata vermez, yanlış cevap verir.

## Fonksiyonlar

| Fonksiyon | Ne döndürür / ne yapar | Maliyet |
|---|---|---|
| `bisect_left(a, x)` | `x`'in girebileceği en soldaki indeks | `O(log n)` |
| `bisect_right(a, x)` (= `bisect`) | `x`'in girebileceği en sağdaki indeks | `O(log n)` |
| `insort_left(a, x)`, `insort(a, x)` | `x`'i sırayı bozmadan ekler | yer `O(log n)`, ekleme `O(n)` |

Hepsi `lo`, `hi` (aramayı bir aralıkla sınırlamak) ve `key=` (Python 3.10'dan
beri) alır.

## Sık kullanımlar

```python
import bisect

a = [10, 20, 20, 20, 30, 40]

# x listede var mı?
i = bisect.bisect_left(a, 20)
found = i < len(a) and a[i] == 20              # True

# x kaç kez geçiyor?
count = bisect.bisect_right(a, 20) - bisect.bisect_left(a, 20)   # 3

# [low, high] aralığında kaç değer var?
in_range = bisect.bisect_right(a, 35) - bisect.bisect_left(a, 15)   # 4

# x'ten büyük ilk değer
j = bisect.bisect_right(a, 25)
first_above = a[j] if j < len(a) else None      # 30
```

## Eşiklere göre sınıflandırma

Not aralıklarını bir sıralı eşik listesine koyup harfi indeksle almak,
uzun bir `if/elif` zincirinden daha kısa:

```python
def letter(score):
    limits = [50, 60, 70, 85]          # bu eşiklerden başlayarak bir üst harf
    letters = ["F", "D", "C", "B", "A"]
    return letters[bisect.bisect_right(limits, score)]

print(letter(49), letter(50), letter(84), letter(85))   # F D B A
```

Eşik değerinin hangi tarafa düştüğüne `bisect_right` mi `bisect_left` mi
kullanacağın karar verir: 50 puan `bisect_right` ile D (eşik dahil üst
dilim), `bisect_left` ile F olurdu.

## Sıralı listeyi canlı tutmak

Sürekli eleman eklenen ve sık sık "x'ten küçük kaç tane var?" diye sorulan
bir liste için `insort` + `bisect` iyi bir ikili. Ekleme `O(n)` olduğu için
milyonlarca eklemede yavaşlar; o noktada öncelik kuyruğu ya da ağaç
yapıları (ileriki bölümler) devreye girer.
