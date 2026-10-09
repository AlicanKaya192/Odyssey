# Python Yapılarının Maliyeti

Python'da tek satırlık işlemler masum görünür: `x in items`,
`items.insert(0, x)`, `items.pop(0)`. Ama bir önceki bölümde gördüğümüz
gibi tek satırın içinde bir döngü saklı olabilir. Hangi yapının hangi işi
ucuza, hangisini pahalıya yaptığını bilmek, çoğu zaman algoritmayı
değiştirmekten bile daha büyük fark yaratır.

Bu bölümde süre de ölçeceğiz. Süre bilgisayara göre değişir; o yüzden
sayıların kendisine değil, **iki yol arasındaki farkın büyüklüğüne** bak.
Aşağıdaki bütün ölçümler bu bilgisayarda alındı.

## Liste nasıl saklanır?

Liste, elemanlarını bellekte **yan yana dizilmiş kutularda** tutar. Bu
yüzden `items[i]` ile bir elemana erişmek, listenin boyu ne olursa olsun
tek adımdır: `O(1)`. Python `i`'inci kutunun yerini hesaplayıp oraya gider.

Peki `append` ile sona eklemek? Liste her eklemede yeniden kurulsa bu `O(n)`
olurdu. Python bunun yerine **fazladan yer ayırır**. Listenin bellekte
kapladığı yeri izleyelim:

```python
import sys

items = []
last = sys.getsizeof(items)
print(0, last)
for i in range(1, 33):
    items.append(i)
    size = sys.getsizeof(items)
    if size != last:
        print(i, size)
        last = size
```

```text
0 56
1 88
5 120
9 184
17 248
25 312
```

32 eklemenin yalnızca birkaçında liste büyüdü (soldaki sayı eleman sayısı,
sağdaki bayt). Büyüdüğü anlarda bütün elemanlar yeni, daha geniş bir yere
kopyalanıyor, bu pahalı; ama ayrılan pay her seferinde büyüdüğü için bu an
giderek seyrekleşiyor. Ortalamaya bakınca her `append` sabit iş: buna
**amortize O(1)** (ortalaması alınmış sabit) denir.

## Baştan eklemek ve çıkarmak: O(n)

Kutular yan yana olduğu için **başa** eleman eklemek, bütün elemanları bir
kutu sağa kaydırmayı gerektirir. Baştan çıkarmak da hepsini bir sola
kaydırır. Listede 50 000 eleman varken bu, her işlemde 50 000 kaydırma.

```python
import time

def measure(func):
    start = time.perf_counter()
    func()
    return round((time.perf_counter() - start) * 1000, 2)   # milisaniye

def add_to_end():
    items = []
    for i in range(50_000):
        items.append(i)

def add_to_front():
    items = []
    for i in range(50_000):
        items.insert(0, i)

print("append    :", measure(add_to_end), "ms")
print("insert(0) :", measure(add_to_front), "ms")
```

```text
append    : 2.3 ms
insert(0) : 334.0 ms
```

Baştan çıkarmak gerektiğinde (bir **kuyruk**: ilk gelen ilk çıkar) Python'un
`collections.deque` yapısı var. `deque` iki ucu da açık bir yapı; iki uçta
da ekleme ve çıkarma `O(1)`:

```python
from collections import deque

def pop_list():
    items = list(range(50_000))
    while items:
        items.pop(0)

def pop_deque():
    items = deque(range(50_000))
    while items:
        items.popleft()

print("list.pop(0)     :", measure(pop_list), "ms")
print("deque.popleft() :", measure(pop_deque), "ms")
```

```text
list.pop(0)     : 254.44 ms
deque.popleft() : 3.73 ms
```

`deque`'in bedeli: ortadaki bir elemana `items[i]` ile erişmek listedeki
kadar hızlı değil. Sırayla işlenen, iki uçtan beslenen işler için doğru
araç.

## `in`: listede arama, kümede bakma

Listede `x in items`, doğrusal arama demektir: baştan sona bakar, `O(n)`.
**Küme (set)** ve **sözlük (dict)** ise elemanları **hash** adı verilen bir
sayıya göre yerleştirir; bir değerin orada olup olmadığına, ortalamada
kümenin boyu ne olursa olsun birkaç adımda bakar: `O(1)`. (Hash'in nasıl
çalıştığı **Hash ile Çözümler** bölümünde.)

```python
numbers_list = list(range(100_000))
numbers_set = set(numbers_list)

def search_list():
    for _ in range(1000):
        -1 in numbers_list

def search_set():
    for _ in range(1000):
        -1 in numbers_set

print("list:", measure(search_list), "ms")
print("set :", measure(search_set), "ms")
```

```text
list: 973.79 ms
set : 0.05 ms
```

Aynı 1000 arama; aradaki fark binlerce kat. Kümenin bedeli: sıra tutmaz,
aynı elemanı iki kez tutmaz, ve yalnızca **değiştirilemeyen** değerler
(sayı, metin, demet) koyulabilir.

## Gizli O(n²)

Bu farkın en sık patladığı yer, bir döngünün içinde listeyle `in`
kullanmak. Bir listedeki tekrarları, sırayı bozmadan ayıklamak isteyelim:

```python
data = list(range(20_000)) * 2      # her sayı iki kez

def unique_with_list():
    result = []
    for value in data:
        if value not in result:      # listede arama: O(n)
            result.append(value)
    return result

def unique_with_set():
    result = []
    seen = set()
    for value in data:
        if value not in seen:        # kümede bakma: O(1)
            seen.add(value)
            result.append(value)
    return result

print("list:", measure(unique_with_list), "ms")
print("set :", measure(unique_with_set), "ms")
print(unique_with_list() == unique_with_set())
```

```text
list: 3816.9 ms
set : 3.51 ms
True
```

İki fonksiyon aynı sonucu veriyor, ama ilki `O(n²)`, ikincisi `O(n)`.
Fark yalnızca bir satır: hangi yapıya `in` diye sorduğumuz. Ek küme `O(n)`
bellek harcıyor; karşılığında saniyeler milisaniyeye iniyor.

## Maliyet tablosu

| İşlem | `list` | `set` / `dict` | `deque` |
|---|---|---|---|
| İndeksle erişim `x[i]` | `O(1)` | yok / anahtarla `O(1)` | `O(n)` |
| Sona ekleme | `O(1)` amortize | `O(1)` | `O(1)` |
| Başa ekleme / baştan çıkarma | `O(n)` | yok | `O(1)` |
| `in` ile arama | `O(n)` | `O(1)` ortalama | `O(n)` |
| Bir değeri silme | `O(n)` | `O(1)` ortalama | `O(n)` |
| Sıra tutar mı? | evet | `set` hayır, `dict` ekleme sırası | evet |

`sort` ve `sorted` `O(n log n)`: verimli sıralama bölümünde neden böyle
olduğunu göreceğiz.

## Metni parça parça kurmak

Python'da metinler (`str`) **değiştirilemez**: `s = s + "x"` her seferinde
yeni bir metin kurar. Çok sayıda parçayı birleştirirken parçaları bir
listede toplayıp en sonda tek seferde `"".join(parts)` ile birleştirmek
hem açık hem güvenli yoldur.

## Özet

- Liste: indeksle erişim ve sona ekleme hızlı; başa ekleme/baştan çıkarma ve
  `in` yavaş (`O(n)`).
- `append` amortize `O(1)`: liste fazladan yer ayırır.
- Kuyruk için `collections.deque`: iki uçta da `O(1)`.
- "İçinde var mı?" sorusu sık soruluyorsa küme ya da sözlük: ortalama `O(1)`.
- Döngünün içindeki tek satırlık `in`, `index`, `count`, `remove` ve
  `insert(0, …)` gizli `O(n)`'dir; toplamı `O(n²)` yapar.
