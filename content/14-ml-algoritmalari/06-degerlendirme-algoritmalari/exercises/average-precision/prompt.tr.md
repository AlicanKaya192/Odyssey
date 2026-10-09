`average_precision(y, score)` fonksiyonunu yaz: puanları büyükten küçüğe
sırala; her konumda kesinlik `TP / konum` ve duyarlılık `TP / pozitif sayısı`;
duyarlılığın her artışını o noktadaki kesinlikle çarpıp topla. `round(..., 4)`.

`average_precision_score` yok.

**Beklenen çıktı:**

```
0.7222
1.0
```
