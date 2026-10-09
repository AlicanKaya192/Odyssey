Ağaç sayı da tahmin eder. Gini yerine **hata kareleri toplamı** küçültülür:
bir bölme, iki tarafın kendi ortalamasına göre kare hatalarının toplamını en
çok düşüren eşiktir. Yaprakta tahmin, oradaki örneklerin ortalaması.

```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(20)
x = rng.uniform(0, 10, 120)
y = np.where(x < 4, 2.0, np.where(x < 7, 5.0, 3.0)) + rng.normal(0, 0.3, 120)


def sse(v):
    return ((v - v.mean()) ** 2).sum()


def best_cut(x, y):
    best_t, best_err = None, sse(y)
    values = np.unique(x)
    for t in (values[:-1] + values[1:]) / 2:
        left = x <= t
        err = sse(y[left]) + sse(y[~left])
        if err < best_err - 1e-12:
            best_t, best_err = t, err
    return best_t


def grow(x, y, depth):
    t = best_cut(x, y) if depth > 0 else None
    if t is None:
        return float(y.mean())                      # yaprak: ortalama
    left = x <= t
    return (t, grow(x[left], y[left], depth - 1), grow(x[~left], y[~left], depth - 1))


def ask(node, v):
    while isinstance(node, tuple):
        node = node[1] if v <= node[0] else node[2]
    return node


tree = grow(x, y, 2)
xq = np.array([1.0, 5.0, 9.0])
ours = np.array([ask(tree, v) for v in xq])
ref = DecisionTreeRegressor(max_depth=2).fit(x[:, None], y).predict(xq[:, None])
print(round(tree[0], 3), ours.round(2), np.allclose(ours, ref))
```

```text
4.008 [1.97 5.   2.95] True
```

Veri basamaklıydı (4'e kadar 2, 7'ye kadar 5, sonra 3). İlk kesim basamaklardan
birinde; üç sorgunun tahmini basamak değerlerine yakın ve scikit-learn'ün
`DecisionTreeRegressor`'ı ile aynı. Regresyon ağacının tahmini **basamaklıdır**:
yaprak sayısı kadar farklı değer verir, aradaki eğimi göremez.
