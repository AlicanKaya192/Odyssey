`estimate_area(n, seed)` fonksiyonunu **Monte Carlo** ile yaz: `y = x²`
eğrisinin `0..1` aralığında altında kalan alanı tahmin etsin (gerçeği `1/3`).
Üreteç `rng = random.Random(seed)`.

`n` kez: önce `x = rng.random()`, sonra `y = rng.random()`; `y <= x * x` ise
nokta eğrinin altında. Tahmin: alttaki nokta sayısı `/ n`, `round(..., 4)`.

**Beklenen çıktı:**

```
100 0.27
10000 0.3392
1000000 0.334
```
