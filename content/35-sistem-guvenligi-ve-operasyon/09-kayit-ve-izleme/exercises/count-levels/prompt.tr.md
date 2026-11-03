Her satır bir JSON kayıt nesnesi ve `level` alanı taşıyor.
`count_levels(lines)` düzey başına satır sayısını `"<DUZEY>: <sayi>"`
satırları olarak, düzey adına göre abece sırasıyla döndürsün. JSON
olarak okunamayan satır programı **durdurmasın**; `INVALID` düzeyinde
sayılsın (bozuk satır da bir işarettir).

**Beklenen çıktı:**

```
ERROR: 1
INFO: 1
INVALID: 1
WARNING: 2
```
