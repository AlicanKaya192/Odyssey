`fit_decay(t, y)` ölçümlere `a * exp(-k * t)` modelini `curve_fit` ile uydursun.
Başlangıç tahmini `p0=[max(y), 0.1]`. `[a, k, yarılanma]` döndürsün:
`a` ve `k` 3 basamak, yarılanma süresi `ln(2) / k` 2 basamak.

**Beklenen çıktı:**

```
[80.203, 0.349, 1.98]
```
