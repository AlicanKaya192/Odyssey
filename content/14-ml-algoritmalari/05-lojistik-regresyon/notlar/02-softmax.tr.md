İkiden çok sınıf varsa her sınıfın kendi ağırlık vektörü olur ve sigmoid
yerine **softmax** kullanılır: `pₖ = e^(zₖ) / Σⱼ e^(zⱼ)`. Bütün olasılıklar
pozitif ve toplamları 1. Gradyan yine aynı sade biçimde: `Aᵀ (P − Y) / n`;
burada `Y` her satırda doğru sınıfın yerinde 1 olan **tek sıcak (one-hot)**
matris.

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(7)
centers = np.array([[0, 0], [3, 0], [0, 3]])
y = rng.integers(0, 3, 240)
X = centers[y] + rng.normal(0, 1.2, size=(240, 2))
A = np.column_stack([np.ones(240), X])
Y = np.eye(3)[y]


def softmax(Z):
    Z = Z - Z.max(axis=1, keepdims=True)
    E = np.exp(Z)
    return E / E.sum(axis=1, keepdims=True)


W = np.zeros((3, 3))
for _ in range(5000):
    P = softmax(A @ W)
    W -= 0.5 * A.T @ (P - Y) / len(y)
P = softmax(A @ W)
ref = LogisticRegression(C=np.inf, max_iter=1000).fit(X, y)
print(round((P.argmax(axis=1) == y).mean(), 3))
print((P.argmax(axis=1) == ref.predict(X)).mean())
print(np.abs(P - ref.predict_proba(X)).max().round(4))
print(P[0].round(3), P[0].sum().round(6))
```

```text
0.908
1.0
0.0002
[0.015 0.002 0.983] 1.0
```

Üç sınıfta doğruluk 0,908; tahminlerin hepsi scikit-learn'ünkiyle aynı ve
olasılıklar en fazla 0,0002 farklı. Softmax'ta en büyük `z`'yi çıkarmak
(`Z - Z.max(...)`) sonucu değiştirmez ama `e^z`'nin taşmasını önler.

Ağırlıkları değil olasılıkları karşılaştırdık: softmax'ta bütün sınıfların
ağırlıklarına aynı vektörü eklemek olasılıkları değiştirmez, yani düzenlileştirme
olmadan ağırlıklar tek değildir.
