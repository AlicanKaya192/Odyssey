Dengesiz veride ROC eğrisi iyimser görünebilir: negatifler çok olduğu için
yüzlerce yanlış pozitif bile FPR'yi az artırır. **Kesinlik-duyarlılık
eğrisi** her eşikte kesinliği ve duyarlılığı çizer; altındaki alanın bir
özeti **ortalama kesinlik (average precision, AP)**: duyarlılığın her
artışında o noktadaki kesinliğin ağırlıklı toplamı.

```python
import numpy as np
from sklearn.metrics import average_precision_score

rng = np.random.default_rng(6)
n = 1000
y = (rng.random(n) < 0.05).astype(int)
score = rng.normal(0, 1, n) + 1.8 * y


def average_precision(y, score):
    ys = y[np.argsort(-score)]
    tp = np.cumsum(ys)
    precision = tp / np.arange(1, len(ys) + 1)
    recall = tp / ys.sum()
    gains = np.diff(np.concatenate([[0], recall]))
    return float((gains * precision).sum())


ours = average_precision(y, score)
print(round(ours, 4), round(average_precision_score(y, score), 4))
print(round(y.mean(), 3))
```

```text
0.3727 0.3727
0.04
```

AP 0,37 civarında; scikit-learn ile aynı. Rastgele bir modelin AP'si pozitif
oranı kadardır (0,04); yani model taban çizgisinin yaklaşık dokuz katı. Aynı
model ROC'ta 0,878 alıyordu: dengesiz veride ROC AUC iyi, AP mütevazı
görünebilir. Pozitifleri bulmak asıl işse AP daha dürüst bir özettir.
