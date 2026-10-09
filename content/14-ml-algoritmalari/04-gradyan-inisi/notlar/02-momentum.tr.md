Dar bir vadide gradyan inişi duvarlar arasında zikzak çizer ve dibe doğru
yavaş ilerler. **Momentum** gradyanları biriktirir: `v ← β v + ∇L`,
`w ← w − η v`. Aynı yöne bakan gradyanlar birbirini güçlendirir, zikzağın
iki yanı birbirini götürür.

```python
import numpy as np

rng = np.random.default_rng(6)
n = 200
X = np.column_stack([rng.uniform(0, 1, n), rng.uniform(0, 10, n)])
y = 1 + 2 * X[:, 0] + 0.5 * X[:, 1] + rng.normal(0, 0.1, n)
A = np.column_stack([np.ones(n), X])
target = ((A @ np.linalg.lstsq(A, y, rcond=None)[0] - y) ** 2).mean()


def steps(lr, beta):
    w, v = np.zeros(3), np.zeros(3)
    for step in range(1, 200_001):
        v = beta * v + 2 / n * A.T @ (A @ w - y)    # beta = 0: düz gradyan inişi
        w -= lr * v
        if ((A @ w - y) ** 2).mean() <= target * 1.01:
            return step
    return None


for lr in (0.001, 0.01):
    print(lr, steps(lr, 0.0), steps(lr, 0.9))
```

```text
0.001 25762 2554
0.01 2575 233
```

Aynı öğrenme oranıyla momentum (`β = 0,9`) yaklaşık on kat az adımda hedefe
ulaştı. Sinir ağlarında kullanılan **Adam** momentuma ek olarak her ağırlık
için adım boyunu kendi gradyan geçmişine göre ayarlar; ölçek farkına karşı
daha da dayanıklıdır.
