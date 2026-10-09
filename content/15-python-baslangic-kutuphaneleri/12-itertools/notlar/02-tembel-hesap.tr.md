`itertools` ve üreteç ifadeleri **tembeldir**: değerleri önceden bir listede
toplamaz, istendikçe birer birer üretir. Bunun iki kazancı var: bellek ve
erken durmak.

## Bellek

```python
import tracemalloc

tracemalloc.start()
total = sum([n * n for n in range(1_000_000)])
list_peak = tracemalloc.get_traced_memory()[1]
tracemalloc.reset_peak()
total2 = sum(n * n for n in range(1_000_000))
gen_peak = tracemalloc.get_traced_memory()[1]
print(total == total2, round(list_peak / 2**20, 1), round(gen_peak / 2**10, 1))
```

```text
True 38.6 4.0
```

`tracemalloc` Python'un ayırdığı belleği ölçer. Köşeli parantezli kavrama
bir milyon kareyi **önce listede topladı**: tepe yaklaşık 38,6 **MB**.
Parantezsiz üreteç ifadesi her kareyi üretip toplama ekledi ve unuttu: tepe
yaklaşık 4 **KB**. Sonuç aynı; bellek dokuz bin kattan fazla az. Değeri bir
kez dolaşacaksan liste kurmana gerek yok.

## Erken durmak ve boru hattı

```python
from itertools import islice

lines = ["4", "", "15", "8", "", "23", "42"]
numbers = (int(line) for line in lines if line.strip())
evens = (n for n in numbers if n % 2 == 0)
print(list(islice(evens, 2)))
```

```text
[4, 8]
```

Üç adım (boş satırları atla, sayıya çevir, çiftleri seç) birbirine bağlı
üreteçler: bir **boru hattı** (pipeline). Hiçbiri tek başına çalışmıyor;
`islice` iki çift sayı isteyince hat yalnızca `4`, `15`, `8`'i işledi ve
**durdu**: `23` ve `42`'ye hiç bakılmadı. Milyonlarca satırlık bir dosyanın
ilk birkaç eşleşmesini ararken bütün dosyayı okumamak böyle olur.

## Ne zaman liste?

| Durum | Seçim |
|---|---|
| Değerleri bir kez dolaşacaksın | üreteç / `itertools` |
| Çok büyük ya da sonsuz akış | üreteç + `islice` |
| İki kez dolaşacaksın, uzunluğu lazım | `list(...)` |
| Rastgele erişim (`x[5]`) | `list(...)` |
| Sıralamak | `sorted(...)` zaten liste verir |
