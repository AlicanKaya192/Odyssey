Bir modelin skoru tek başına bir şey söylemez: %89 doğruluk iyi mi? Bunu
anlamanın yolu, **hiçbir şey öğrenmeyen** bir modelle karşılaştırmaktır.
scikit-learn'de bunun hazır sınıfı var: `DummyClassifier` (ve
`DummyRegressor`).

```python
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=5, weights=[0.9],
                           random_state=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3)
base = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
model = LogisticRegression().fit(X_train, y_train)
print(round(y_test.mean(), 3))
print(round(base.score(X_test, y_test), 3), round(model.score(X_test, y_test), 3))
flagged = [int(m.predict(X_test).sum()) for m in (base, model)]
print(*flagged, int(y_test.sum()))
```

```text
0.108
0.892 0.94
0 18 27
```

## Ne oldu?

- Test setinde pozitif sınıfın payı %10,8. Hep "0" diyen taban çizgisi bu
  yüzden **%89,2** doğruluk alıyor, ama tek bir pozitifi bile bulmuyor
  (tahmin ettiği pozitif sayısı 0).
- Gerçek model %94: taban çizgisinden yalnızca 5 puan iyi. 27 pozitiften 18
  tanesini işaretledi (bazıları yanlış olabilir; ayrıntısı metrikler
  bölümünde).
- Ders: **dengesiz** veride doğruluk yanıltıcıdır. Her yeni model önce taban
  çizgisiyle karşılaştırılır; onu geçemeyen model hiçbir şey öğrenmemiştir.

## Taban çizgisi türleri

| Sınıf | `strategy` | Ne yapar |
|---|---|---|
| `DummyClassifier` | `"most_frequent"` | hep en sık sınıf |
| `DummyClassifier` | `"stratified"` | sınıf oranlarıyla rastgele |
| `DummyRegressor` | `"mean"` / `"median"` | hep ortalama / medyan |

Taban çizgisi de bir scikit-learn modelidir: aynı `fit` / `predict` /
`score` arayüzü, aynı çapraz doğrulama ve metrik araçları.
