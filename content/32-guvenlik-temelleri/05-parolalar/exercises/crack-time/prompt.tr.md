`crack_time(bits, guesses_per_second)` rastgele bir parolanın ortalama
bulunma süresini okunur bir biçimde versin.

- Ortalama süre (saniye): `2 ** (bits - 1) / guesses_per_second`.
- Birimler büyükten küçüğe: `"years"` (31 536 000 sn), `"days"` (86 400),
  `"hours"` (3 600), `"minutes"` (60), `"seconds"` (1).
- Sürenin **1'e eşit ya da büyük** çıktığı ilk birimi seç ve `(deger, birim)`
  demeti döndür; `deger` `round(..., 1)`.
- Süre bir saniyeden de kısaysa birim `"seconds"` olsun.

**Beklenen çıktı:**

```
(1743.3, 'years')
(55.0, 'seconds')
(1.6, 'days')
(0.0, 'seconds')
```
