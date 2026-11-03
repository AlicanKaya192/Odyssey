`detector_scores(alerts, attacks)` uyarı verilen ve gerçekten saldırı olan
olay kimliklerinden (iki liste) `[kesinlik, duyarlilik]` döndürsün, ikisi
de 2 basamağa yuvarlanmış. Kesinlik `TP / (TP + FP)`, duyarlılık
`TP / (TP + FN)`. Payda 0 ise o değer `0.0` olsun.

**Beklenen çıktı:**

```
[0.5, 0.67]
[0.0, 0.0]
```
