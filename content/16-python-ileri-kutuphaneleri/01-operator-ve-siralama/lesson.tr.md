# operator ve Sıralama

Sıralamak her programda var: en çok satan ürünler, en yeni kayıtlar, ada
göre kişiler. `sorted` ile basit bir listeyi sıralamayı biliyorsun. Bu bölüm
gerçek verideki soruları cevaplıyor: sözlükleri bir alana göre, birden çok
alana göre, biri artan biri azalan, büyük/küçük harfe bakmadan sıralamak;
yalnızca ilk birkaçını almak; sıralı bir listeye sırayı bozmadan eklemek.
Araçlar `sorted`'ın `key` parametresi, **`operator`** modülü, **`heapq`** ve
**`bisect`**.

## sorted ve list.sort

```python
nums = [5, 2, 9, 1]
result = sorted(nums)
print(result, nums)
print(nums.sort(), nums)
print(sorted("banana"), sorted({"b": 1, "a": 2}))
```

```text
[1, 2, 5, 9] [5, 2, 9, 1]
None [1, 2, 5, 9]
['a', 'a', 'a', 'b', 'n', 'n'] ['a', 'b']
```

- **`sorted(x)`** yeni bir liste döndürür, aslına dokunmaz; her
  dolaşılabilir şeyi alır (metin harf harf, sözlük anahtarlarıyla).
- **`list.sort()`** listeyi **yerinde** sıralar ve `None` döndürür:
  `x = x.sort()` yazmak listeyi kaybettirir.

## key: neye göre?

```python
words = ["banana", "Cherry", "apple", "Date"]
print(sorted(words))
print(sorted(words, key=str.casefold))
print(sorted(words, key=len, reverse=True))
people = [{"name": "Ada", "age": 36}, {"name": "Alan", "age": 41},
          {"name": "Grace", "age": 36}]
print([p["name"] for p in sorted(people, key=lambda p: p["age"])])
```

```text
['Cherry', 'Date', 'apple', 'banana']
['apple', 'banana', 'Cherry', 'Date']
['banana', 'Cherry', 'apple', 'Date']
['Ada', 'Grace', 'Alan']
```

- Metinler varsayılan olarak karakter numarasıyla sıralanır: **büyük harfler
  küçüklerden önce** gelir (`Cherry`, `apple`'dan önce).
- **`key`** her eleman için bir kez çağrılan fonksiyondur; sıralama onun
  döndürdüğü değere göre yapılır. `str.casefold` harf büyüklüğünü yok sayar,
  `len` uzunluğa göre dizer.
- `reverse=True` tersine çevirir. Eşit anahtarlı elemanlar **geldikleri
  sırayı korur**: `banana` ve `Cherry` ikisi de 6 harfli, ilk gelen önde.
- Sözlük listesi bir alana göre: `key=lambda p: p["age"]`.

## operator: itemgetter ve attrgetter

```python
from collections import namedtuple
from operator import attrgetter, itemgetter

rows = [("book", 3, 12.0), ("ink", 10, 0.5), ("pen", 3, 1.5)]
print(sorted(rows, key=itemgetter(1)))
print(sorted(rows, key=itemgetter(1, 2)))
Item = namedtuple("Item", "name stock price")
items = [Item(*row) for row in rows]
print([i.name for i in sorted(items, key=attrgetter("price"), reverse=True)])
print(itemgetter(0, 2)(rows[0]))
```

```text
[('book', 3, 12.0), ('pen', 3, 1.5), ('ink', 10, 0.5)]
[('pen', 3, 1.5), ('book', 3, 12.0), ('ink', 10, 0.5)]
['book', 'pen', 'ink']
('book', 12.0)
```

- **`itemgetter(1)`** `lambda r: r[1]` ile aynı işi yapar; daha kısa ve
  daha hızlı. Sözlükte `itemgetter("age")`.
- **`itemgetter(1, 2)`** demet döndürür: önce stoğa, stok eşitse fiyata göre.
  Stoğu 3 olan iki üründen ucuz olan (`pen`) öne geçti.
- **`attrgetter("price")`** nesnelerin özelliğine göre (`namedtuple`, sınıf).
- `itemgetter(0, 2)` tek başına da kullanılır: satırdan iki alanı birlikte
  çeker.

## Birden çok alan, farklı yönler

```python
from operator import itemgetter

scores = [("ada", "math", 90), ("alan", "math", 85),
          ("grace", "cs", 90), ("linus", "cs", 85)]
by_score = sorted(scores, key=itemgetter(2), reverse=True)
print([s[0] for s in by_score])
two_pass = sorted(by_score, key=itemgetter(1))
print([s[0] for s in two_pass])
print([s[0] for s in sorted(scores, key=lambda s: (s[1], -s[2]))])
```

```text
['ada', 'grace', 'alan', 'linus']
['grace', 'linus', 'ada', 'alan']
['grace', 'linus', 'ada', 'alan']
```

"Derse göre artan, aynı derste puana göre azalan" iki yoldan yapılır:

- **İki geçiş:** önce **ikincil** alana (puan, azalan), sonra **birincil**
  alana (ders) göre sırala. Python'un sıralaması **kararlıdır** (stable):
  ikinci sıralamada eşit kalanlar ilk sıralamadaki düzenini korur.
- **Tek anahtar:** `(ders, -puan)` demeti. Sayıda yönü çevirmek için eksi
  işareti yeter; metin alanında eksi olmadığı için iki geçiş kullanılır.

## heapq ve bisect

```python
import bisect
import heapq

prices = [42, 7, 19, 88, 3, 56, 21]
print(heapq.nlargest(3, prices), heapq.nsmallest(2, prices))
for score in [33, 99, 77, 70, 89, 90]:
    print(score, "FDCBA"[bisect.bisect([60, 70, 80, 90], score)])
ordered = [10, 20, 30]
bisect.insort(ordered, 25)
print(ordered, bisect.bisect_left(ordered, 25), bisect.bisect_left(ordered, 26))
```

```text
[88, 56, 42] [3, 7]
33 F
99 A
77 C
70 C
89 B
90 A
[10, 20, 25, 30] 2 3
```

- **`heapq.nlargest(n, x)`** / **`nsmallest`**: bütün listeyi sıralamadan
  en büyük / en küçük `n` eleman. Büyük veride "ilk 10" için `sorted(...)[:10]`'dan
  hızlıdır; `key` de alır.
- **`bisect`** sıralı bir listede bir değerin **nereye gireceğini** ikili
  aramayla bulur. Not sınırları `[60, 70, 80, 90]` listesinde puanın yeri,
  harf listesinde indeks oldu: 70 tam sınırda `C` (bisect sınırın sağına
  koyar).
- **`bisect.insort`** değeri sırayı bozmadan ekler; her eklemeden sonra
  `sort()` çağırmaya gerek kalmaz. `bisect_left` değerin ilk yerini verir.

## Sık hatalar

```python
from functools import cmp_to_key

try:
    sorted([3, "a", 1])
except TypeError as error:
    print("TypeError:", error)
values = [3, None, 1]
print(sorted(values, key=lambda v: (v is None, v)))


def compare(a, b):
    return len(a) - len(b) or (a > b) - (a < b)


print(sorted(["bb", "a", "ccc", "ab"], key=cmp_to_key(compare)))
```

```text
TypeError: '<' not supported between instances of 'str' and 'int'
[1, 3, None]
['a', 'ab', 'bb', 'ccc']
```

- Python 3 metinle sayıyı karşılaştırmaz: karışık liste `TypeError` verir.
  Önce türleri birleştir ya da `key` ile ortak bir değere çevir.
- `None` içeren listede `(v is None, v)` anahtarı `None`'ları sona atar:
  önce demetin ilk elemanı (`False < True`) karşılaştırılır, `None` hiç
  sayıyla karşılaştırılmaz.
- Eski kodda "iki elemanı karşılaştıran fonksiyon" (cmp) görürsün;
  **`cmp_to_key`** onu `key`'e çevirir. Yeni kodda doğrudan `key` yaz:
  buradaki karşılaştırma `key=lambda s: (len(s), s)` ile aynı.

## Özet

- `sorted` yeni liste, `list.sort()` yerinde ve `None`.
- `key=` her eleman için bir kez; `str.casefold`, `len`, `lambda`,
  `itemgetter`, `attrgetter`.
- Kararlı sıralama: çok alanlı sıralama iki geçişle ya da demet anahtarla;
  sayıda yön için eksi.
- `heapq.nlargest` / `nsmallest` ilk n için; `bisect` sıralı listede yer
  bulmak, `insort` sırayı bozmadan eklemek.
