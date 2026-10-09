Naive Bayes özelliklerin sınıf içinde bağımsız olduğunu varsayar. Aynı bilgiyi
taşıyan özellikler olunca (fiyat ve vergili fiyat gibi) model o kanıtı birkaç
kez sayar. En uç hâli: aynı özelliği kopyalamak.

```python
import numpy as np
from sklearn.naive_bayes import GaussianNB

rng = np.random.default_rng(19)
y = rng.integers(0, 2, 400)
x = rng.normal(0, 1, 400) + 1.0 * y
Xt = np.array([[0.8]])
for copies in (1, 3, 10):
    # aynı özelliğin kopyaları
    X = np.repeat(x[:, None], copies, axis=1)
    p = GaussianNB().fit(X, y).predict_proba(np.repeat(Xt, copies, axis=1))[0, 1]
    print(copies, round(p, 3))
yt = rng.integers(0, 2, 2000)
xt = rng.normal(0, 1, 2000) + yt
for copies in (1, 10):
    X = np.repeat(x[:, None], copies, axis=1)
    m = GaussianNB().fit(X, y)
    p = m.predict_proba(np.repeat(xt[:, None], copies, axis=1))[:, 1]
    accuracy = ((p > 0.5) == yt).mean()
    # olasılığın kare hatası
    brier = np.mean((p - yt) ** 2)
    print(copies, round(float(accuracy), 3), round(float(brier), 3))
```

```text
1 0.591
3 0.7
10 0.926
1 0.696 0.198
10 0.7 0.265
```

Aynı örnek için sınıf 1 olasılığı tek özellikle 0,591, on kopyayla 0,926:
yeni bilgi yok ama model çok daha emin. Doğruluk değişmiyor (0,696 → 0,7),
çünkü karar sınırı aynı yerde; ama olasılıkların kalitesini ölçen **Brier
puanı** (olasılığın kare hatası) 0,198'den 0,265'e kötüleşiyor. Naive Bayes
sınıflandırmada iyi, olasılıkları ise çoğu zaman aşırı emindir; olasılık
gerekiyorsa sonradan kalibre edilir ya da birbirine çok benzeyen özellikler
ayıklanır.
