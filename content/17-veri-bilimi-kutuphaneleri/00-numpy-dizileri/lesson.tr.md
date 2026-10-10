# NumPy Dizileri ve Veri Tipleri

Veri Bilimi patikasında NumPy dizisini kurdun, seçtin, topladın. Bu modül
aynı kütüphanelerin **perde arkasına** iniyor. İlk durak dizinin veri tipi
(dtype): bir dizinin her elemanı aynı tipte ve aynı boyda saklanır. Bu,
NumPy'yi hızlı yapan şey; ama yanlış tip seçilince sayılar **sessizce**
bozulur, metinler kırpılır, bellek boşa gider. Bu bölüm o sessiz hataları
ölçerek gösteriyor.

## Her dizinin bir dtype'ı var

```python
import numpy as np

a = np.array([1, 2, 3])
print(a.dtype, a.itemsize, a.nbytes)
print(np.array([1.5, 2, 3]).dtype)
mixed = np.array([1, 2.5, "x"])
print(mixed.dtype, mixed)
print(np.array([1, None]).dtype)
```

```text
int64 8 24
float64
<U32 ['1' '2.5' 'x']
object
```

- **`dtype`** elemanların tipi, **`itemsize`** bir elemanın bayt boyu,
  **`nbytes`** dizinin toplam boyu. Bu bilgisayarda tam sayıların
  varsayılanı `int64`: eleman başına 8 bayt.
- Tipler karışınca NumPy hepsini taşıyabilecek **tek** tipe çıkar: bir ondalık
  varsa her şey `float64`.
- Bir metin karışırsa **her şey metne** döner (`<U32`: en fazla 32 karakterlik
  Unicode). Sayılar artık sayı değil; toplamaya kalkınca hata alırsın.
- `None` karışırsa `object`: elemanlar sıradan Python nesnesi olarak
  saklanır ve NumPy'nin hızı kaybolur.

## Taşma: sessizce bozulan sayılar

```python
import numpy as np

print(np.iinfo(np.int8).min, np.iinfo(np.int8).max)
small = np.array([100, 120], dtype=np.int8)
print(small + small, (small + small).dtype)
print(np.array([300]).astype(np.int8))
print(np.iinfo(np.int64).max)
```

```text
-128 127
[-56 -16] int8
[44]
9223372036854775807
```

- **`int8`** −128 ile 127 arasını tutar. `100 + 100 = 200` sığmıyor; sonuç
  **uyarısız** `-56` oldu (taşan değer başa sarar). Python'un kendi `int`'inde
  böyle bir sınır yok; NumPy'de var.
- **`astype(np.int8)`** 300'ü `44` yaptı, yine uyarısız.
- **`np.iinfo(tip)`** bir tam sayı tipinin sınırlarını verir; ondalıklar için
  `np.finfo`.
- Kural: küçük tip **bellek** kazandırır (aşağıda) ama yalnızca değerlerin
  sığacağı **kesin** ise kullanılır. Toplama, çarpma sonucu da sığmalı.

## float32 ve duyarlık

```python
import numpy as np

print(np.finfo(np.float32).eps, np.finfo(np.float64).eps)
count = np.float32(16_777_217)
print(count, int(count))
print(np.float64(16_777_217) == 16_777_217)
```

```text
1.1920929e-07 2.220446049250313e-16
1.6777216e+07 16777216
True
```

- **`float32`** yaklaşık 7, **`float64`** yaklaşık 16 anlamlı basamak tutar;
  `eps` 1'den büyük en küçük sayı ile 1 arasındaki fark.
- 16 777 217 `float32`'ye sığmıyor: en yakın değer 16 777 216. Büyük
  sayaçlar, kimlik numaraları, kuruş cinsinden tutarlar `float32`'de **bozulur**.
- `float32` derin öğrenmede yaygın (yarı bellek, ekran kartında hızlı);
  istatistik ve para için `float64` (ya da decimal bölümündeki yollar).

## Bellek: doğru tip, küçük dizi

```python
import numpy as np

big = np.arange(1_000_000)
print(big.nbytes // 1024, big.astype(np.int32).nbytes // 1024,
      big.astype(np.int16).nbytes // 1024)
names = np.array(["ab", "cde"])
print(names.dtype)
names[0] = "hello"
print(names)
```

```text
7812 3906 1953
<U3
['hel' 'cde']
```

- Bir milyon `int64` 7812 KB; `int32` yarısı, `int16` dörtte biri. Değerler
  sığıyorsa tip küçültmek belleği doğrudan böler (bu milyon sayı `int16`'ya
  sığmaz, burada yalnızca boyu gösteriyoruz).
- **Metin dizisinin genişliği sabit:** `["ab", "cde"]` dizisi `<U3`, yani en
  fazla 3 karakter. `"hello"` atanınca **sessizce** `"hel"` oldu. Değişken
  uzunlukta metin için pandas'ın metin sütunu ya da `dtype=object` kullanılır.

## Dizi kurmanın yolları

```python
import numpy as np

print(np.arange(0, 1, 0.25))
print(np.linspace(0, 1, 5))
print(np.full((2, 2), 7))
print(np.eye(3, dtype=int))
print(np.zeros_like(np.array([1, 2, 3])), np.ones(3, dtype=bool))
```

```text
[0.   0.25 0.5  0.75]
[0.   0.25 0.5  0.75 1.  ]
[[7 7]
 [7 7]]
[[1 0 0]
 [0 1 0]
 [0 0 1]]
[0 0 0] [ True  True  True]
```

- **`arange(başla, bitir, adım)`**: bitiş dahil değil. Ondalık adımda kaç
  eleman çıkacağı yuvarlama yüzünden şaşırtabilir; o yüzden ondalık aralık
  için **`linspace(başla, bitir, adet)`** tercih edilir (bitiş dahil).
- **`full(şekil, değer)`**, **`eye(n)`** (birim matris), **`zeros` / `ones`**.
- **`*_like(dizi)`** aynı şekil ve tipte yeni dizi kurar.
- Her kurucu `dtype=` alır; baştan doğru tip, sonradan `astype`'tan ucuzdur.

## Şekil, görünüm ve kopya

```python
import numpy as np

m = np.arange(12).reshape(3, 4)
print(m.shape, m.ndim, m.size, m.strides)
flat_view = m.ravel()
flat_view[0] = 99
flat_copy = m.flatten()
flat_copy[1] = -1
print(m[0, :3])
print(np.shares_memory(m, flat_view), np.shares_memory(m, flat_copy))
print(np.arange(6).reshape(2, -1).shape)
try:
    m.reshape(5, 3)
except ValueError as error:
    print("ValueError:", error)
```

```text
(3, 4) 2 12 (32, 8)
[99  1  2]
True False
(2, 3)
ValueError: cannot reshape array of size 12 into shape (5,3)
```

- **`shape`** boyutlar, **`ndim`** boyut sayısı, **`size`** eleman sayısı.
  **`strides`** bir sonraki satıra / sütuna geçmek için bellekte kaç bayt
  atlanacağı: satır 32 bayt (4 × 8), sütun 8 bayt. NumPy şekil değiştirmeyi
  çoğu zaman yalnızca bu sayıları değiştirerek, veriyi kopyalamadan yapar.
- **`ravel()`** mümkünse **görünüm** (view) döndürür: aynı belleğe bakar,
  ona yazmak `m`'yi değiştirdi (`99`). **`flatten()`** her zaman **kopya**:
  ona yazmak `m`'ye dokunmadı.
- **`np.shares_memory(a, b)`** iki dizinin aynı belleği paylaşıp
  paylaşmadığını söyler; "bu kopya mı?" sorusunun kesin cevabı.
- `reshape`'te **`-1`** "geri kalanı sen hesapla" demek. Eleman sayısı
  tutmazsa `ValueError`.

## Eksik değer ve tam sayı

```python
import numpy as np

print(np.nan == np.nan, np.isnan(np.array([1.0, np.nan])))
counts = np.array([3, 4, 5])
try:
    counts[0] = np.nan
except ValueError as error:
    print("ValueError:", error)
print(np.array([3, np.nan, 5]).dtype)
```

```text
False [False  True]
ValueError: cannot convert float NaN to integer
float64
```

- **`NaN` kendisine bile eşit değil**; eksik değer `np.isnan` ile aranır.
- NaN bir **ondalık** değer: tam sayı dizisine konamaz. Eksik değer içeren bir
  sayı sütunu bu yüzden `float64` olur. (pandas'ın `Int64` gibi tipleri bunu
  çözer; pandas performansı bölümünde.)

## Özet

- Her dizinin tek bir `dtype`'ı var; karışık girdi en geniş tipe çıkar
  (metin ve `None` dahil).
- Tam sayı dizileri taşınca **uyarısız** başa sarar; `iinfo` sınırları
  söyler. `astype` da sessizce bozar.
- `float32` ~7 basamak; büyük sayıyı bozar.
- Doğru tip belleği böler; metin dizisinin genişliği sabittir.
- `ravel` görünüm, `flatten` kopya; emin olmak için `np.shares_memory`.
- NaN ondalıktır, tam sayı dizisine girmez.
