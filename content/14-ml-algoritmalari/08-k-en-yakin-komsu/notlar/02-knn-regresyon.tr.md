KNN yalnızca sınıflandırmada değil, sayı tahmininde de kullanılır: en yakın
`k` örneğin hedeflerinin **ortalaması** tahmindir. Bir seçenek daha var:
**uzaklıkla ağırlıklandırmak**; yakın komşunun oyu `1 / uzaklık` kadar sayılır.

```python
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

rng = np.random.default_rng(18)
x = np.sort(rng.uniform(0, 10, 80))
y = np.sin(x) + rng.normal(0, 0.2, 80)
xq = np.array([2.5, 5.0, 7.5])


def knn_reg(x, y, xq, k, weighted=False):
    out = []
    for q in xq:
        d = np.abs(x - q)
        near = np.argsort(d)[:k]
        if weighted:
            w = 1 / d[near]                       # yakın olan çok sayılır
            out.append((w * y[near]).sum() / w.sum())
        else:
            out.append(y[near].mean())                     # düz ortalama
    return np.array(out)


for weighted, mode in ((False, "uniform"), (True, "distance")):
    ours = knn_reg(x, y, xq, 7, weighted)
    model = KNeighborsRegressor(n_neighbors=7, weights=mode)
    ref = model.fit(x[:, None], y).predict(xq[:, None])
    print(mode, ours.round(3), np.allclose(ours, ref))
print(np.sin(xq).round(3))
```

```text
uniform [ 0.563 -0.779  0.873] True
distance [ 0.491 -0.878  0.956] True
[ 0.598 -0.959  0.938]
```

İki yöntem de scikit-learn'ün `KNeighborsRegressor`'ı ile aynı. Son satır
gerçek değer (`sin x`). Uzaklık ağırlığı üç noktanın ikisinde (5 ve 7,5)
gerçeğe daha yakın, birinde (2,5) değil: tepe ve çukurlarda yakın komşular
daha doğru bilgi taşır, ama ağırlık gürültüye de daha duyarlıdır. Hangisinin
iyi olduğu yine çapraz doğrulamayla görülür.
