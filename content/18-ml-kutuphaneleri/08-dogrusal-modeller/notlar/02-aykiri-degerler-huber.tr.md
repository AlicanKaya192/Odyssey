Doğrusal regresyon hataların **karesini** küçültür. 60 birim sapan tek bir
kayıt, 1 birim sapan 3600 kayıt kadar ağır basar; birkaç hatalı kayıt
doğruyu kendine çeker. `HuberRegressor` küçük hatalarda kareyi, büyüklerde
mutlak değeri kullanır: uzaktaki noktanın çekişi sınırlı kalır.

```python
import numpy as np
from sklearn.linear_model import HuberRegressor, LinearRegression

rng = np.random.default_rng(4)
x = rng.uniform(0, 10, 100)
y = 2 * x + 1 + rng.normal(0, 1, 100)    # gerçek: eğim 2, sabit 1
y[:5] += 60                              # 5 hatalı kayıt
X = x.reshape(-1, 1)
for model in [LinearRegression(), HuberRegressor()]:
    model.fit(X, y)
    slope, const = float(model.coef_[0]), float(model.intercept_)
    print(type(model).__name__, round(slope, 2), round(const, 2))
```

```text
LinearRegression 2.38 2.11
HuberRegressor 2.03 1.11
```

## Ne görüyoruz

- 100 kaydın 5'i bozuk. Doğrusal regresyon eğimi 2,38, sabiti 2,11 buldu:
  bütün doğru yukarı kaydı.
- Huber 2,03 ve 1,11 buldu, gerçeğe çok yakın.

## Ne zaman

- Hedefte ara sıra ölçüm/kayıt hatası varsa ve onları tek tek temizlemek
  mümkün değilse.
- Hatalı kayıtlar bulunabiliyorsa önce onları düzelt; Huber bir temizlik
  aracı değil, sigorta.
- Hata ölçüsü olarak da MAE, MSE'ye göre aykırı değerlerden daha az
  etkilenir; aynı fikir.
