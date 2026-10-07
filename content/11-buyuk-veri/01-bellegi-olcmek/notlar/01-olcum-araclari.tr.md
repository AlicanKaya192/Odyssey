Bu patikada kullanacağın ölçüm araçlarının hepsi bu sayfada. Hepsi bayt
döndürüyor; megabayt için `/ 1024**2`.

## Tablo ve sütun

| Kod | Ne veriyor |
|---|---|
| `df.info(memory_usage="deep")` | Sütunlar, türler, boş olmayan sayısı ve gerçek toplam boyut |
| `df.memory_usage(deep=True)` | Sütun başına bayt; ilk satır `Index` |
| `df.memory_usage(deep=True).sum()` | Tablonun tamamı |
| `df.memory_usage(deep=True).drop("Index")` | Yalnızca sütunlar |
| `df["city"].memory_usage(deep=True)` | Tek sütun (indeks dahil) |
| `df.index.memory_usage()` | Yalnızca indeks |
| `array.nbytes` | NumPy dizisi |

## Hazır rapor

```python
memory = df.memory_usage(deep=True).drop("Index")
report = pd.DataFrame({
    "mb": (memory / 1024**2).round(2),
    "share": (memory / memory.sum() * 100).round(1),
    "per_row": (memory / len(df)).round(1),
})
print(report.sort_values("mb", ascending=False))
```

`per_row` 8'den çok büyükse o sütun ya metin ya da yanlış türde.

## Dosya

```python
import os

os.path.getsize("orders.csv")     # bayt
```

## Tepe bellek

```python
import tracemalloc

tracemalloc.start()
# ... ölçülecek kod ...
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
```

- `current`: şu anda ayrılmış olan.
- `peak`: `start()`'tan bu yana en yüksek değer.
- Yalnızca Python nesnelerini ve NumPy dizilerini görür; pandas 3'ün `str`
  sütunlarını görmez.
- `tracemalloc.reset_peak()`: tepeyi sıfırlar, aynı oturumda iki işlemi ayrı
  ayrı ölçmek için.

## Süre

```python
import time

start = time.perf_counter()
# ... ölçülecek kod ...
seconds = time.perf_counter() - start
```

`time.time()` değil `time.perf_counter()`: kısa süreleri daha hassas
ölçüyor ve sistem saati değişse bile şaşmıyor.

## Bu tablonun ölçümleri (100 000 sipariş)

| Sütun | Tür | Satır başına bayt |
|---|---|---|
| `order_time` | `str` | 27,0 |
| `city` | `str` | 14,5 |
| `category` | `str` | 14,3 |
| `payment` | `str` | 12,8 |
| `order_id`, `customer_id`, `quantity` | `int64` | 8 |
| `unit_price` | `float64` | 8 |

Toplam 9,6 MB; metin sütunları %68,2.
