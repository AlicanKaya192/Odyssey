`predict_one(xs, ys, x)` tek özellikli verilerle (`xs`, `ys`) bir
`LinearRegression` eğitsin ve `x` için tahmini 2 basamağa yuvarlı `float`
olarak döndürsün. Hem eğitim verisi hem tahmin girdisi **iki boyutlu**
olmalı: `np.array(xs).reshape(-1, 1)` ve `[[x]]`. Başlangıç kodu tek boyutlu
veriyor ve duruyor.

**Beklenen çıktı:**

```
21.0
```
