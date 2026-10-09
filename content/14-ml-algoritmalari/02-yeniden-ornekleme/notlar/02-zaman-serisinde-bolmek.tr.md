Zamana bağlı veride (satışlar, sensör ölçümleri) karıştırmak geleceği
geçmişe sızdırır. **İleriye doğru (forward chaining)** ayrımda eğitim kümesi
her katta büyür ve test hep ondan sonra gelir.

```python
import numpy as np
from sklearn.model_selection import TimeSeriesSplit


def time_splits(n, k):
    size = n // (k + 1)
    for i in range(1, k + 1):
        train = np.arange(0, i * size + n % (k + 1))
        test = np.arange(len(train), len(train) + size)
        yield train, test


n = 20
for train, test in time_splits(n, 4):
    print(train.min(), train.max(), "|", test.min(), test.max())
ours = [(tr.tolist(), te.tolist()) for tr, te in time_splits(n, 4)]
splitter = TimeSeriesSplit(n_splits=4)
theirs = [(tr.tolist(), te.tolist()) for tr, te in splitter.split(np.zeros(n))]
print(ours == theirs)
```

```text
0 3 | 4 7
0 7 | 8 11
0 11 | 12 15
0 15 | 16 19
True
```

Her katta eğitim 0'dan başlıyor ve büyüyor; test hemen arkasından geliyor.
scikit-learn'ün `TimeSeriesSplit`'i ile aynı katlar. Zaman Serileri
patikasındaki "kayan başlangıçlı doğrulama" bu fikrin genelleşmiş hâli.
