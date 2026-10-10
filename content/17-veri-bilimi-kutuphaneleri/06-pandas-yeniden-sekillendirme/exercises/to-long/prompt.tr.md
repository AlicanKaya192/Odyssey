`to_long(rows, months)` her satırı `[şehir, ay1, ay2, ...]` olan geniş bir
tablo alıyor; sütun adları `["city", *months]`. `melt` ile uzun biçime
çevirip (`var_name="month"`, `value_name="sales"`) satırları
`[şehir, ay, satış]` listesi olarak döndürsün (`.values.tolist()`).
**Döngü yazma.**

**Beklenen çıktı:**

```
['Izmir', 'jan', 80]
['Ankara', 'jan', 120]
['Izmir', 'feb', 95]
['Ankara', 'feb', 110]
```
