## Bir grubun oranı ve standart hatası

```python
import numpy as np


def ratio_and_se(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    r = y.mean() / x.mean()
    var = (y.var(ddof=1) - 2 * r * np.cov(x, y)[0, 1]
           + r ** 2 * x.var(ddof=1)) / (len(x) * x.mean() ** 2)
    return round(float(r), 4), round(float(np.sqrt(var)), 4)


views = [1, 2, 10, 40, 3]
clicks = [1, 1, 2, 4, 0]
print(ratio_and_se(views, clicks))
print(round(float(np.mean(np.array(clicks) / np.array(views))), 4))
```

```text
(0.1429, 0.0433)
0.36
```

İlk satır toplamların oranı ve delta standart hatası, ikinci satır
kullanıcı oranlarının ortalaması. Aynı veri, çok farklı iki "oran": 40
gösterimli kullanıcı ilkinde ağır basıyor, ikincisinde her kullanıcı tek
oy.

## İki grubun farkı

- Fark: R_B − R_A.
- Standart hata: √(var_A + var_B) (gruplar bağımsız).
- z = fark / standart hata, p = 2 · (1 − Φ(|z|)).

## Formülün parçaları

| Simge | Anlamı |
|---|---|
| n | kullanıcı sayısı (gösterim değil) |
| X̄, Ȳ | kullanıcı başına ortalama gösterim ve tıklama |
| s_X², s_Y² | kullanıcı düzeyinde varyanslar |
| s_XY | kullanıcı düzeyinde kovaryans |
| R | Ȳ / X̄ |
