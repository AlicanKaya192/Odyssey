`safe_sqrt(values)` eksi olmayan değerlerin karekökünü alsın, eksi
değerlerin yerine `-1.0` yazsın. `np.sqrt(..., where=..., out=...)` kullan:
`out` başlangıçta `-1.0` dolu bir dizi (`np.full`). Sonucu liste olarak
döndür.

**Beklenen çıktı:**

```
[2.0, -1.0, 3.0, -1.0, 0.0]
```
