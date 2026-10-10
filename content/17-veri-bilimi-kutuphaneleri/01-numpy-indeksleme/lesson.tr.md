# NumPy İndeksleme

Veri Bilimi patikasında dilimlemeyi, fancy index'i ve koşullu seçimi gördün.
Bu bölüm iki boyutlu ve daha karmaşık seçimlere iniyor: satır ve sütunu
birlikte seçmek, bir seçimin **görünüm mü kopya mı** olduğunu bilmek
(yazınca aslının değişip değişmeyeceği), koşulları birleştirmek ve
`where`, `argsort`, `unique` gibi "nerede?" sorusuna cevap veren araçlar.

## İki boyutta seçim

```python
import numpy as np

m = np.arange(1, 13).reshape(3, 4)
print(m)
print(m[1, 2], m[:, 1])
print(m[1:, ::2].tolist())
```

```text
[[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]]
7 [ 2  6 10]
[[5, 7], [9, 11]]
```

- **`m[satır, sütun]`**: virgülle iki eksen birden. `m[1][2]` de aynı sonucu
  verir ama önce bütün satırı çıkarır; `m[1, 2]` doğrudan gider ve ikinci
  eksende dilim (`m[:, 1]`) ancak bu yazımla mümkün.
- **`m[:, 1]`**: bütün satırların 1. sütunu.
- **`m[1:, ::2]`**: 1. satırdan sona, sütunlarda ikişer atlayarak.

## Satır listesi ve sütun listesi: iki farklı anlam

```python
import numpy as np

m = np.arange(1, 13).reshape(3, 4)
print(m[[0, 2], [1, 3]])
print(m[np.ix_([0, 2], [1, 3])])
```

```text
[ 2 12]
[[ 2  4]
 [10 12]]
```

- **İki listeyle seçim çiftleri eşler:** `m[[0, 2], [1, 3]]` (0, 1) ve
  (2, 3) konumlarını alır: **iki eleman**, alt matris değil. En sık yapılan
  NumPy hatalarından biri.
- **Alt matris** (bu satırlar × bu sütunlar) için **`np.ix_`**: dört eleman,
  2 × 2.

## Görünüm mü kopya mı?

```python
import numpy as np

m = np.arange(1, 13).reshape(3, 4)
part = m[0:2, 0:2]
part[0, 0] = 100
print(m[0, 0], np.shares_memory(m, part))
m[0, 0] = 1
picked = m[[0, 1]]
picked[0, 0] = -5
print(m[0, 0], np.shares_memory(m, picked))
m[m > 10][0] = 999
print(m.max())
m[m > 10] = 0
print(m[2].tolist())
```

```text
100 True
1 False
12
[9, 10, 0, 0]
```

- **Dilim (`:`) görünümdür:** `part`'a yazmak `m`'yi değiştirdi.
- **Liste ya da maske ile seçim (fancy index) kopyadır:** `picked`'e yazmak
  `m`'ye dokunmadı.
- **Zincirleme atama işe yaramaz:** `m[m > 10][0] = 999` önce bir **kopya**
  çıkarıyor, sonra kopyanın ilk elemanını değiştiriyor; `m` aynı kaldı (en
  büyük hâlâ 12).
- **Tek adımda atama çalışır:** `m[m > 10] = 0` doğrudan `m`'ye yazar. Kural:
  maskeyi ya da listeyi **atamanın sol tarafında, tek köşeli parantezde**
  kullan.

## Koşulları birleştirmek

```python
import numpy as np

v = np.array([5, -3, 8, 0, -1, 7])
print(v[(v > 0) & (v < 8)])
print(v[~(v > 0)])
print(v[(v < 0) | (v == 8)])
try:
    v[v > 0 and v < 8]
except ValueError as error:
    print("ValueError:", str(error)[:46])
```

```text
[5 7]
[-3  0 -1]
[-3  8 -1]
ValueError: The truth value of an array with more than one
```

- Maskeler **`&`** (ve), **`|`** (veya), **`~`** (değil) ile birleşir; her
  koşul **parantez** içinde: `&` karşılaştırmadan önce işlendiği için
  `v > 0 & v < 8` yanlış okunur.
- Python'un `and` / `or` / `not` sözcükleri dizide çalışmaz: tek bir
  `True` / `False` bekler, diziyle ne yapacağını bilemez (`ValueError`).

## Nerede? where, nonzero, argsort

```python
import numpy as np

v = np.array([5, -3, 8, 0, -1, 7])
print(np.where(v > 0, v, 0))
print(np.where(v < 0)[0], np.nonzero(v)[0])
order = np.argsort(v)
print(order, v[order][::-1][:3])
scores = np.array([[3, 90], [1, 75], [2, 82]])
print(scores[scores[:, 1].argsort()[::-1]].tolist())
print(np.argmax(np.array([[1, 9, 3], [7, 2, 8]]), axis=1))
```

```text
[5 0 8 0 0 7]
[1 4] [0 1 2 4 5]
[1 4 3 0 5 2] [8 7 5]
[[3, 90], [2, 82], [1, 75]]
[1 2]
```

- **`np.where(koşul, a, b)`**: koşul doğruysa `a`, değilse `b`; eleman
  eleman "if-else". Tek argümanla (`np.where(koşul)`) doğru olan
  **konumları** verir (demet; `[0]` ile ilk eksen).
- **`np.nonzero(v)`**: sıfır olmayanların konumu.
- **`np.argsort(v)`** değerleri değil, değerleri sıralayacak **sırayı**
  (indeksleri) verir. `v[order]` sıralı dizi; `[::-1][:3]` en büyük üçü.
- **Bir sütuna göre satır sıralamak:** o sütunun `argsort`'u ile bütün
  satırlar seçilir; burada puana göre büyükten küçüğe.
- **`argmax(axis=1)`**: her satırda en büyüğün sütun konumu.

## unique, isin, clip, newaxis

```python
import numpy as np

labels = np.array(["b", "a", "b", "c", "b"])
values, counts = np.unique(labels, return_counts=True)
print(values, counts)
print(np.isin(np.array([1, 2, 3, 4]), [2, 4]))
print(np.clip(np.array([5, -3, 8, 0]), 0, 5))
x = np.array([1, 2, 3])
print(x[:, np.newaxis].shape, x[np.newaxis, :].shape)
```

```text
['a' 'b' 'c'] [1 3 1]
[False  True False  True]
[5 0 5 0]
(3, 1) (1, 3)
```

- **`np.unique(..., return_counts=True)`**: sıralı benzersiz değerler ve
  kaçar kez geçtikleri.
- **`np.isin(dizi, liste)`**: her eleman listede var mı (SQL'deki `IN`).
- **`np.clip(dizi, alt, üst)`**: sınırların dışını sınıra çeker.
- **`np.newaxis`** (`None` ile aynı) yeni bir boyut ekler: `(3,)` → `(3, 1)`
  sütun, `(1, 3)` satır. Bir sonraki bölümdeki yayınlamanın anahtarı.

## Özet

- `m[satır, sütun]`; `m[:, j]` sütun.
- İki listeyle seçim **çift** eşler; alt matris için `np.ix_`.
- Dilim görünüm, liste/maske kopya; zincirleme atama (`m[maske][0] = …`)
  aslını değiştirmez, `m[maske] = …` değiştirir.
- Maskeler `&`, `|`, `~` ve parantez; `and`/`or` değil.
- `where` (koşullu değer / konum), `argsort` (sıralama sırası), `argmax`,
  `unique`, `isin`, `clip`, `newaxis`.
