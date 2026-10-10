# Yayınlama ve ufunc

NumPy'de `dizi * 2` yazınca 2 her elemana uygulanır; `matris - satır` yazınca
satır her satırdan çıkarılır. Bu **yayınlama** (broadcasting): şekilleri
farklı iki dizi, küçük olan kopyalanmadan büyüğün şekline "yayılarak"
işleme girer. Arkasındaki eleman eleman çalışan fonksiyonlar da **ufunc**
(evrensel fonksiyon). Bu bölüm yayınlamanın kurallarını, en sık hatasını
(`keepdims`) ve ufunc'ların az bilinen güçlerini anlatıyor.

## Kural: sağdan karşılaştır

```python
import numpy as np

col = np.array([[1], [2], [3]])
row = np.array([10, 20, 30, 40])
print(col.shape, row.shape, (col + row).shape)
print(col + row)
print(np.broadcast_shapes((5, 3), (3,)), np.broadcast_shapes((3, 1), (1, 4)))
```

```text
(3, 1) (4,) (3, 4)
[[11 21 31 41]
 [12 22 32 42]
 [13 23 33 43]]
(5, 3) (3, 4)
```

İki şekil **sağdan** eksen eksen karşılaştırılır. Her eksende ya iki boy
**eşit** olmalı ya da biri **1** olmalı; 1 olan diğerinin boyuna yayılır.
Eksik eksen başa 1 olarak eklenir.

- `(3, 1)` + `(4,)` → `(4,)` önce `(1, 4)` olur; sonra iki eksende de biri 1:
  sonuç `(3, 4)`. Sütun her satıra, satır her sütuna yayıldı.
- `(5, 3)` + `(3,)`: son eksenler eşit (3), `(3,)` beş satıra yayılır. Bir
  satırı bütün satırlardan çıkarmak tam olarak budur.
- **Kopya yapılmaz:** NumPy küçük diziyi bellekte çoğaltmaz, adım
  (stride) olarak 0 kullanır.

## Sütun bazında ölçeklemek

```python
import numpy as np

X = np.array([[1.0, 200], [2, 400], [3, 600]])
Z = (X - X.mean(axis=0)) / X.std(axis=0)
print(X.mean(axis=0).shape)
print(Z.round(2).tolist())
```

```text
(2,)
[[-1.22, -1.22], [0.0, 0.0], [1.22, 1.22]]
```

- `X.mean(axis=0)` her **sütunun** ortalaması: şekil `(2,)`. `(3, 2)` ile
  `(2,)` sağdan uyar; ortalama her satırdan çıkarılır.
- Sonuç standartlaştırılmış veri: her sütun ortalaması 0, sapması 1. Makine
  öğrenmesinin `StandardScaler`'ı içeride tam bunu yapar.

## En sık hata: satır bazında ve keepdims

```python
import numpy as np

X = np.array([[1.0, 200], [2, 400], [3, 600]])
print(X.sum(axis=1).shape)
try:
    X / X.sum(axis=1)
except ValueError as error:
    print("ValueError:", str(error).strip())
share = X / X.sum(axis=1, keepdims=True)
print(X.sum(axis=1, keepdims=True).shape)
print(share.round(3).tolist())
```

```text
(3,)
ValueError: operands could not be broadcast together with shapes (3,2) (3,)
(3, 1)
[[0.005, 0.995], [0.005, 0.995], [0.005, 0.995]]
```

- Her satırı kendi toplamına bölmek istiyoruz. `X.sum(axis=1)` şekli `(3,)`;
  sağdan karşılaştırınca `X`'in son ekseni (2) ile 3 uymuyor: **hata**.
  (Satır sayısı ile sütun sayısı eşit olsaydı hata bile çıkmaz, **yanlış**
  eksene bölerdi; daha tehlikeli.)
- **`keepdims=True`** toplanan ekseni silmez, 1 olarak bırakır: `(3, 1)`.
  Artık her satıra kendi toplamı yayılıyor.
- Kural: **satır bazında** (axis=1) işlemde `keepdims=True`; sütun bazında
  (axis=0) gerekmez.

## Herkesle herkes: uzaklık matrisi

```python
import numpy as np

points = np.array([[0, 0], [3, 4], [6, 8]])
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
print(diff.shape)
distance = np.sqrt((diff ** 2).sum(axis=-1))
print(distance.tolist())
```

```text
(3, 3, 2)
[[0.0, 5.0, 10.0], [5.0, 0.0, 5.0], [10.0, 5.0, 0.0]]
```

- `(3, 1, 2)` − `(1, 3, 2)` → `(3, 3, 2)`: her noktanın her noktaya farkı,
  **döngüsüz**. Karelerin son eksende toplamı ve karekökü uzaklık matrisi.
- k-en yakın komşu, kümeleme gibi algoritmaların içi böyle hesaplanır
  (Algoritmalar patikası, ML Algoritmaları modülü).
- Bedel bellek: n nokta için n × n × boyut; çok büyük n'de parça parça
  hesaplanır.

## ufunc'ların gizli yetenekleri

```python
import numpy as np

print(np.add.reduce([1, 2, 3, 4]), np.add.accumulate([1, 2, 3, 4]))
print(np.multiply.outer([1, 2], [10, 20, 30]).tolist())
print(np.maximum([1, 5, 3], [4, 2, 6]), np.maximum.reduce([3, 9, 2]))
out = np.empty(3)
np.multiply([1, 2, 3], 2, out=out)
print(out)
v = np.array([1.0, -2.0, 4.0])
print(np.sqrt(v, where=v >= 0, out=np.full(3, np.nan)))
```

```text
10 [ 1  3  6 10]
[[10, 20, 30], [20, 40, 60]]
[4 5 6] 9
[2. 4. 6.]
[ 1. nan  2.]
```

- Her ufunc'ın metotları var: **`reduce`** (hepsini birleştir: toplam),
  **`accumulate`** (birikimli), **`outer`** (her çift: çarpım tablosu).
- **`np.maximum`** iki diziyi eleman eleman karşılaştırır (`np.max` bir
  dizinin en büyüğü; ikisi farklı).
- **`out=`** sonucu var olan diziye yazar: büyük döngülerde her seferinde
  yeni dizi kurulmaz.
- **`where=`** yalnızca koşulun doğru olduğu yerlerde hesaplar; eksi sayının
  karekökü uyarı vermeden atlanır (`out` başlangıçta `nan`).

## Python fonksiyonunu vektörleştirmek?

```python
import timeit

import numpy as np

data = np.random.default_rng(1).normal(size=200_000)
vector = min(timeit.repeat(lambda: data * 2 + 1, number=1, repeat=3))
loop = min(timeit.repeat(lambda: [x * 2 + 1 for x in data], number=1, repeat=3))
wrapped = np.vectorize(lambda x: x * 2 + 1)
vectorized = min(timeit.repeat(lambda: wrapped(data), number=1, repeat=3))
print(loop / vector > 10, vectorized / vector > 10)
```

```text
True True
```

- Dizi işlemi (`data * 2 + 1`) döngüden bu bilgisayarda yaklaşık 36 kat hızlı.
- **`np.vectorize`** bir Python fonksiyonunu diziye uygulanır yapar, ama adı
  yanıltıcı: içeride yine döngü; hızı döngüye yakın (dizi işleminden ~27 kat
  yavaş). Yalnızca kolaylık içindir.
- Hız için ifadeyi dizi işlemleriyle (`np.where`, `np.clip`, ufunc'lar)
  yeniden yaz.

## Özet

- Yayınlama: şekiller sağdan karşılaştırılır; eşit ya da 1. Küçük dizi
  kopyalanmadan yayılır.
- Sütun bazında `X - X.mean(axis=0)`; satır bazında `keepdims=True` şart.
- `[:, np.newaxis]` ile "herkesle herkes" hesapları döngüsüz.
- ufunc metotları: `reduce`, `accumulate`, `outer`; `out=` ve `where=`.
- `np.vectorize` hız kazandırmaz.
