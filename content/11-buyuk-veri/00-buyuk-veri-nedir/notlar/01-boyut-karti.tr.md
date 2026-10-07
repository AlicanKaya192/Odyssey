Bir tablonun ne kadar yer tutacağını kâğıt üzerinde tahmin etmek için
gereken her şey bu sayfada. Tahmin iyi bir başlangıç; kesin sayı için yine
`memory_usage(deep=True)` ile ölç.

## Birimler

| Birim | Bayt | Python'da |
|---|---|---|
| 1 KB | 1 024 | `1024` |
| 1 MB | 1 048 576 | `1024**2` |
| 1 GB | 1 073 741 824 | `1024**3` |
| 1 TB | 1 099 511 627 776 | `1024**4` |

Bayttan megabayta: `bayt / 1024**2`. Gigabayttan bayta: `gb * 1024**3`.

Disk üreticileri 1 GB = 10⁹ bayt sayıyor; bu yüzden "1 TB" disk Windows'ta
931 GB görünüyor.

## Bir değer kaç bayt?

| Tür | Bayt | Tutabildiği |
|---|---|---|
| `bool` | 1 | `True` / `False` |
| `int8` | 1 | -128 … 127 |
| `uint8` | 1 | 0 … 255 |
| `int16` | 2 | -32 768 … 32 767 |
| `int32` | 4 | yaklaşık ±2,1 milyar |
| `int64` | 8 | yaklaşık ±9,2 × 10¹⁸ |
| `float32` | 4 | yaklaşık 7 basamak duyarlılık |
| `float64` | 8 | yaklaşık 15–16 basamak duyarlılık |
| `datetime64[ns]` | 8 | nanosaniye duyarlı tarih-saat |

pandas bir CSV'yi okurken tam sayıları `int64`, ondalıklıları `float64`
yapıyor. Daha küçük türlere geçmek Bölüm 2'nin konusu.

**Metin sabit genişlikte değil.** Her hücre metnin uzunluğu kadar yer
tutuyor; bu yüzden metin sütununun boyutunu ancak ölçerek bilebilirsin.

## Hızlı hesap

```text
boyut (bayt) ≈ satır × sayı sütunu × 8
```

| Satır | Sayı sütunu | Yaklaşık |
|---|---|---|
| 1 milyon | 10 | 76 MB |
| 10 milyon | 6 | 458 MB |
| 100 milyon | 10 | 7,5 GB |
| 1 milyar | 6 | 44,7 GB |

Metin sütunları bunun üstüne eklenir.

## Ölçmek için

```python
import os

os.path.getsize("orders.csv")             # dosya, bayt
df.memory_usage(deep=True)                # sütun sütun, bayt
df.memory_usage(deep=True).sum()          # tablo, bayt
array.nbytes                              # NumPy dizisi, bayt
```

## Bu patikanın ölçümleri (1 milyon sipariş)

| | Boyut |
|---|---|
| CSV dosyası | 61,1 MB |
| pandas 3, `str` metin | 95,9 MB |
| eski `object` metin | 252,3 MB |
| 1 milyon sayı, Python listesi | 34,3 MB |
| 1 milyon sayı, NumPy dizisi | 7,6 MB |
