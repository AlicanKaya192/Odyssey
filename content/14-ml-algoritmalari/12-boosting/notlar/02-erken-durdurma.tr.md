Boosting'de ağaç sayısı aşırı uyumun düğmesi. Doğru sayıyı bulmanın
pratik yolu **erken durdurma (early stopping)**: eğitimin bir parçasını
doğrulama için ayır, her ağaçtan sonra doğrulama hatasına bak, belli bir
sayıda tur iyileşme olmazsa dur.

```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(22)
X = rng.uniform(0, 10, (300, 1))
y = np.sin(X[:, 0]) * 3 + rng.normal(0, 0.8, 300)
Xtr, ytr, Xval, yval = X[:200], y[:200], X[200:], y[200:]

pred_tr = np.full(200, ytr.mean())
pred_val = np.full(100, ytr.mean())
best, best_n, waited = np.inf, 0, 0
for n in range(1, 1001):
    tree = DecisionTreeRegressor(max_depth=3).fit(Xtr, ytr - pred_tr)
    pred_tr += 0.1 * tree.predict(Xtr)
    pred_val += 0.1 * tree.predict(Xval)
    val = ((yval - pred_val) ** 2).mean()
    if val < best - 1e-9:
        best, best_n, waited = val, n, 0
    else:
        waited += 1
    if waited == 30:                                  # 30 tur iyileşme yok
        break
print(best_n, n, round(best, 3), round(val, 3))
```

```text
45 75 0.743 0.758
```

Doğrulama hatası en düşük değerine birinci sütundaki ağaç sayısında ulaştı;
30 tur sabırla bekledikten sonra eğitim ikinci sütundaki turda durdu. Son
hata en iyiden biraz yüksek: model en iyi turdaki ağaç sayısıyla kullanılır.
Bin ağaç kurmak yerine çok daha azında duruldu. scikit-learn'de
`GradientBoostingRegressor(n_iter_no_change=..., validation_fraction=...)` ve
`HistGradientBoosting*` aynı fikri uygular.
