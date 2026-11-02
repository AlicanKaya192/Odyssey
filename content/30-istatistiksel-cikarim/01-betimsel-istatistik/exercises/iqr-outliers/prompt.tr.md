`iqr_outliers(values)` 1,5 × IQR kuralının dışında kalan değerleri sıralı bir
liste olarak döndürsün. `q1, q3 = np.percentile(values, [25, 75])`,
`iqr = q3 - q1`; alt sınır `q1 - 1.5 * iqr`, üst sınır `q3 + 1.5 * iqr`.
Sınırların **dışındakiler** (küçük ya da büyük) aykırı.

**Beklenen çıktı:**

```text
[100]
[-40]
```
