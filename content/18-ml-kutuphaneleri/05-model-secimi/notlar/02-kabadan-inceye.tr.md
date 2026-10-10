`C` ve `gamma` gibi ayarların doğru değeri 0,001 de olabilir 1000 de. Düz
aralıklı bir ızgara (1, 2, 3, ...) bu genişliği kaplayamaz. Kullanılan yol:
önce **log ölçekte kaba** bir ızgara, sonra en iyi çıkan noktanın çevresinde
**ince** bir ızgara.

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

X, y = make_classification(n_samples=400, n_features=10, n_informative=4,
                           random_state=12)
coarse = {"C": np.logspace(-3, 3, 7), "gamma": np.logspace(-4, 1, 6)}
first = GridSearchCV(SVC(), coarse, cv=5).fit(X, y)
c0, g0 = first.best_params_["C"], first.best_params_["gamma"]
print(round(float(c0), 4), round(float(g0), 4), round(first.best_score_, 3))
steps = np.logspace(-0.5, 0.5, 5)
fine = {"C": c0 * steps, "gamma": g0 * steps}
second = GridSearchCV(SVC(), fine, cv=5).fit(X, y)
best = second.best_params_
c1, g1 = float(best["C"]), float(best["gamma"])
print(round(c1, 3), round(g1, 4), round(second.best_score_, 3))
print(len(first.cv_results_["params"]) + len(second.cv_results_["params"]))
```

```text
10.0 0.1 0.952
31.623 0.0316 0.962
67
```

## Adımlar

1. **Kaba:** `np.logspace(-3, 3, 7)` = 0,001, 0,01, ..., 1000. Her adım 10 kat.
   42 kombinasyonda en iyisi `C=10`, `gamma=0,1`.
2. **İnce:** o noktanın yarım basamak (√10 ≈ 3,16 kat) altı ve üstü, 5'er
   değer. En iyisi `C≈31,6`, `gamma≈0,032`; skor 0,952'den 0,962'ye çıktı.
3. Toplam 67 kombinasyon. Aynı inceliği tek bir ızgarayla bütün aralıkta
   aramak yüzlerce kombinasyon isterdi.

## Dikkat

- En iyi değer kaba ızgaranın **kenarına** düşerse (`C=1000` gibi), aralık
  yetmemiştir; o yönde genişlet.
- İnce aramadaki kazanç (burada 0,01) çoğu zaman katlar arası sapmadan
  küçüktür ve iyimserliği artırır. Kaba aramanın bulduğu bölge çoğu zaman
  yeterlidir.
