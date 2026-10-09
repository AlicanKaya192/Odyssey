# itertools

Döngülerle yazılan bazı kalıplar her projede yeniden kurulur: iki listeyi
uç uca eklemek, ardışık elemanları ikişer ikişer almak, birikimli toplam,
bir listeyi parçalara bölmek, bütün ikili kombinasyonlar... **`itertools`**
bunların hepsini hazır, hızlı ve **tembel** (lazy) olarak verir: sonuçları
önceden bir listede toplamaz, istendikçe birer birer üretir. Python
patikasında gördüğün üreteçlerle (generator) aynı mantık.

`itertools` fonksiyonları **yineleyici** (iterator) döndürür; ekranda görmek
için `list(...)` ile listeye çeviriyoruz.

## Sonsuz yineleyiciler ve islice

```python
from itertools import count, cycle, islice, repeat

print(list(islice(count(10, 5), 4)))
print(list(islice(cycle("AB"), 5)))
print(list(repeat("x", 3)))
for i, color in zip(range(4), cycle(["red", "green"])):
    print(i, color)
```

```text
[10, 15, 20, 25]
['A', 'B', 'A', 'B', 'A']
['x', 'x', 'x']
0 red
1 green
2 red
3 green
```

- **`count(başla, adım)`** sonsuza kadar sayar; **`cycle`** bir diziyi
  sonsuza kadar döndürür. Sonsuz oldukları için tek başlarına `list(...)`
  yapılmaz; bilgisayar belleği bitene kadar dener.
- **`islice(yineleyici, n)`** ilk `n` elemanı alır: yineleyicilerin dilimi.
- `zip` en kısa dizide durduğu için `cycle` ile güvenle eşleşir: satırlara
  sırayla renk vermek gibi.

## Birleştirmek, eşleştirmek, bölmek

```python
from itertools import batched, chain, pairwise, zip_longest

print(list(chain([1, 2], (3, 4), "ab")))
names, scores = ["a", "b", "c"], [1, 2]
print(list(zip(names, scores)), list(zip_longest(names, scores, fillvalue=0)))
print(list(pairwise([10, 13, 9, 20])))
print([b - a for a, b in pairwise([10, 13, 9, 20])])
print(list(batched(range(7), 3)))
```

```text
[1, 2, 3, 4, 'a', 'b']
[('a', 1), ('b', 2)] [('a', 1), ('b', 2), ('c', 0)]
[(10, 13), (13, 9), (9, 20)]
[3, -4, 11]
[(0, 1, 2), (3, 4, 5), (6,)]
```

- **`chain`** dizileri kopyalamadan uç uca dolaşır.
- `zip` kısa dizide durur ve `c`'yi kaybeder; **`zip_longest`** eksikleri
  `fillvalue` ile doldurur.
- **`pairwise`** ardışık ikilileri verir: ardışık farklar (günlük değişim
  gibi) için ideal.
- **`batched(dizi, n)`** `n`'erli parçalara böler; son parça kısa olabilir.
  Bir API'ye kayıtları 100'erli göndermek gibi (Python 3.12'den beri).

## Birikim ve süzme

```python
import operator
from itertools import accumulate, compress, dropwhile, takewhile

sales = [5, 3, 8, 2, 7]
print(list(accumulate(sales)))
print(list(accumulate(sales, max)))
print(list(accumulate(sales, operator.mul)))
print(list(takewhile(lambda x: x < 8, sales)))
print(list(dropwhile(lambda x: x < 8, sales)))
print(list(compress("ABCDE", [1, 0, 1, 0, 1])))
```

```text
[5, 8, 16, 18, 25]
[5, 5, 8, 8, 8]
[5, 15, 120, 240, 1680]
[5, 3]
[8, 2, 7]
['A', 'C', 'E']
```

- **`accumulate`** birikimli toplamı verir (5, 5+3, 5+3+8...). İkinci argüman
  başka bir işlem: `max` ile "o ana kadarki en yüksek", `operator.mul` ile
  birikimli çarpım.
- **`takewhile`** koşul tuttuğu sürece alır, ilk tutmayanda **durur**;
  **`dropwhile`** o ana kadar atlar, sonrasının hepsini verir. `filter`'dan
  farkı: koşul bir kez bozulunca geri dönülmez.
- **`compress`** yanındaki listede doğru olanları seçer.

## groupby: ardışık grupları toplamak

```python
from itertools import groupby

words = ["apple", "avocado", "banana", "blueberry", "cherry", "apricot"]
for letter, group in groupby(words, key=lambda w: w[0]):
    print(letter, list(group))
print("---")
for letter, group in groupby(sorted(words), key=lambda w: w[0]):
    print(letter, list(group))
print([(k, len(list(g))) for k, g in groupby("aaabccdddd")])
```

```text
a ['apple', 'avocado']
b ['banana', 'blueberry']
c ['cherry']
a ['apricot']
---
a ['apple', 'apricot', 'avocado']
b ['banana', 'blueberry']
c ['cherry']
[('a', 3), ('b', 1), ('c', 2), ('d', 4)]
```

**`groupby`** yalnızca **yan yana duran** aynı anahtarlıları bir araya
getirir: `apricot` sonda olduğu için `a` grubu iki kez çıktı. Bütün
grupları istiyorsan önce **aynı anahtarla sırala**. Son satır ardışık
tekrarları sayıyor (`aaab...` → `a` 3 kez): basit sıkıştırma ve "kaç gün üst
üste" sorularında kullanılır. Sıralamak istemiyorsan önceki bölümdeki
`defaultdict(list)` daha uygun.

## Kombinatorik

```python
import math
from itertools import (combinations, combinations_with_replacement,
                       permutations, product)

print(list(product("AB", [1, 2])))
print(sum(1 for _ in product(range(10), repeat=3)))
print(list(permutations("ABC", 2)))
print(list(combinations("ABCD", 2)))
print(list(combinations_with_replacement("AB", 2)))
print(sum(1 for _ in combinations(range(20), 6)), math.comb(20, 6))
```

```text
[('A', 1), ('A', 2), ('B', 1), ('B', 2)]
1000
[('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]
[('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'D')]
[('A', 'A'), ('A', 'B'), ('B', 'B')]
38760 38760
```

| Fonksiyon | Ne üretir | Sıra önemli mi | Tekrar |
|---|---|---|---|
| `product(a, b)` | her `a` ile her `b` | evet | evet |
| `product(x, repeat=3)` | üç haneli şifre gibi | evet | evet |
| `permutations(x, k)` | `k`'lı dizilişler | evet | hayır |
| `combinations(x, k)` | `k`'lı gruplar | hayır | hayır |
| `combinations_with_replacement(x, k)` | tekrarlı gruplar | hayır | evet |

Üç haneli kilidin 1000 olasılığı `product` ile, 20 kişiden 6 kişilik grup
sayısı `combinations` ile sayıldı; sonuç `math.comb` ile aynı. Kombinasyon
sayısı çok hızlı büyür: bütün olasılıkları denemek ancak küçük girdilerde
mümkündür.

## Sık hata: yineleyici bir kez tükenir

```python
from itertools import islice

numbers = map(int, ["1", "2", "3"])
print(sum(numbers), sum(numbers))
it = iter(range(10))
print(list(islice(it, 3)), list(islice(it, 3)))
squares = (n * n for n in range(5))
print(list(squares), list(squares))
```

```text
6 0
[0, 1, 2] [3, 4, 5]
[0, 1, 4, 9, 16] []
```

Yineleyici bir kez dolaşılır: `map`'in ilk `sum`'u 6 verdi, ikincisi 0.
`islice` aynı yineleyiciden **devam etti** (0–2, sonra 3–5). Sonuca iki kez
ihtiyacın varsa bir kez `list(...)` yap ve listeyi kullan.

## Özet

- `count`, `cycle`, `repeat` sonsuz; `islice` ile sınırla.
- `chain` uç uca, `zip_longest` eksikleri doldurur, `pairwise` ardışık
  ikililer, `batched` parçalar.
- `accumulate` birikim; `takewhile` / `dropwhile` koşul bozulana kadar;
  `compress` seçer.
- `groupby` yalnızca yan yana olanları gruplar: önce sırala.
- `product`, `permutations`, `combinations`.
- Yineleyiciler bir kez tükenir; tekrar gerekiyorsa listeye çevir.
