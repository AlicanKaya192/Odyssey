MultiIndex yalnızca satırlarda olmaz. `agg`'e sütun başına birden fazla
fonksiyon verince **sütunlar** iki düzeyli olur ve sonraki adımda
`report["sales_sum"]` gibi bir şey yazmak hata verir.

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["Izmir", "Izmir", "Ankara", "Ankara", "Bursa"],
    "sales": [80, 95, 120, 110, 50],
    "returns": [2, 5, 4, 1, 0],
})
report = df.groupby("city").agg({"sales": ["sum", "mean"], "returns": ["sum"]})
print(report.columns.tolist())
print(report)
print(report[("sales", "sum")].tolist())
report.columns = ["_".join(pair) for pair in report.columns]
print(report.columns.tolist())
named = df.groupby("city").agg(total=("sales", "sum"), avg=("sales", "mean"))
print(named.columns.tolist())
```

```text
[('sales', 'sum'), ('sales', 'mean'), ('returns', 'sum')]
       sales        returns
         sum   mean     sum
city                       
Ankara   230  115.0       5
Bursa     50   50.0       0
Izmir    175   87.5       7
[230, 50, 175]
['sales_sum', 'sales_mean', 'returns_sum']
['total', 'avg']
```

## Üç yol

1. **Demetle seçmek:** sütun adı artık `("sales", "sum")` demeti.
   `report[("sales", "sum")]` çalışır, ama her yerde demet yazmak yorucu.
2. **Düzleştirmek:** `"_".join(pair)` her demeti tek ada çevirir:
   `sales_sum`, `sales_mean`, `returns_sum`. Rapor CSV'ye ya da Excel'e
   gidecekse bu en temiz yol; iki satırlı başlık oralarda kötü görünür.
3. **Adlandırılmış toplama:** `agg(total=("sales", "sum"), ...)` en baştan tek
   düzeyli sütun verir ve adı sen seçersin. Yeni kodda önerilen yazım budur.

## Ne zaman MultiIndex'li sütun iyi?

Aynı ölçüleri birçok grup için yan yana görmek istediğinde (her şehir için
toplam ve ortalama) iki düzeyli başlık okunaklıdır ve
`report["sales"]` tek hamlede iki sütunu birden getirir. Ama tablo başka bir
araca ya da modele gidecekse düzleştir.
