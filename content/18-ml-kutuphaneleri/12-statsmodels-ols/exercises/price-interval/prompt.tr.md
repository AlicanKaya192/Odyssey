`price_interval(area, age)` tek bir ev için tahmini ve **tek gözlem** aralığını
döndürsün: `[ortalama, obs_alt, obs_üst]` (1 basamak). Başlangıç kodu tek
satırlık veride `sm.add_constant`'ı varsayılanla çağırıyor; `const` eklenmiyor
ve tahmin hata veriyor.

**Beklenen çıktı:**

```
[330.9, 256.9, 405.0]
```
