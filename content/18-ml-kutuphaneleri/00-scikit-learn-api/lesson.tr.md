# scikit-learn API'si

scikit-learn'de yüzden fazla model ve dönüştürücü var; hepsini ayrı ayrı
öğrenmek gerekmez, çünkü hepsi **aynı arayüzü** kullanır: kur, `fit` ile
veriden öğren, sonra `predict` ya da `transform` ile kullan. Bu arayüzü bir
kez kavrayan biri yeni bir modeli belgesine beş dakika bakarak kullanabilir.
Bu bölüm o ortak sözleşmeyi, öğrenilen değerlerin nerede durduğunu ve en sık
iki hatayı (eğitilmemiş model, yanlış şekilli girdi) anlatıyor; sonunda
modül boyunca dönüp duracağımız **veri sızıntısı** fikri var.

## fit, transform, predict

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

X = np.array([[1.0, 200], [2.0, 220], [3.0, 400], [4.0, 410]])
y = np.array([0, 0, 1, 1])
scaler = StandardScaler()
Xs = scaler.fit_transform(X)
print(scaler.mean_.tolist(), Xs.mean(axis=0).round(6).tolist())
model = LogisticRegression()
model.fit(Xs, y)
print(model.predict(Xs).tolist(), model.score(Xs, y))
print(model.predict_proba(Xs[:1]).round(3).tolist())
```

```text
[2.5, 307.5] [0.0, 0.0]
[0, 0, 1, 1] 1.0
[[0.852, 0.148]]
```

| Metot | Kimde | Ne yapar |
|---|---|---|
| `fit(X, y)` | hepsi | veriden öğrenir, nesnenin kendisini döndürür |
| `transform(X)` | dönüştürücüler | öğrendiğini veriye uygular |
| `fit_transform(X)` | dönüştürücüler | ikisi birden |
| `predict(X)` | modeller | tahmin |
| `predict_proba(X)` | sınıflandırıcıların çoğu | sınıf olasılıkları |
| `score(X, y)` | modeller | varsayılan ölçü (sınıflandırmada doğruluk, regresyonda R²) |

- `X` her zaman **iki boyutlu**: satırlar örnek, sütunlar özellik. `y` tek
  boyutlu hedef.
- Dönüştürücü (`StandardScaler`) ile model (`LogisticRegression`) aynı
  `fit` kalıbını kullanıyor. Bu yüzden ileride ikisini bir **Pipeline**'da
  arka arkaya bağlayabileceğiz.
- `predict_proba` her sınıf için olasılık verir: ilk örnek %85,2 olasılıkla 0.

## Ayarlar ve öğrenilenler

```python
from sklearn.base import clone
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(C=0.5, max_iter=500)
print(model.get_params()["C"], model.get_params()["max_iter"])
model.set_params(C=2.0)
print(model.C, hasattr(model, "coef_"))
twin = clone(model)
print(twin.C, twin is model)
```

```text
0.5 500
2.0 False
2.0 False
```

- Kurucuya verilenler **hiperparametre**dir: modelin nasıl öğreneceğini
  sen seçersin (`C`, `max_iter`). `get_params` / `set_params` ile okunur ve
  değiştirilir; hiperparametre aramaları bunu kullanır.
- Veriden **öğrenilenler** sonunda alt çizgi taşır: `coef_`, `mean_`,
  `classes_`. `fit`'ten önce yoktur (`hasattr` → `False`).
- `clone` aynı ayarlarla **eğitilmemiş** yeni bir kopya kurar. Çapraz
  doğrulama her katta modeli böyle sıfırdan kurar.

## İki sık hata

```python
import numpy as np
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LinearRegression

model = LinearRegression()
try:
    model.predict(np.array([[1.0]]))
except NotFittedError as error:
    print(type(error).__name__ + ":", str(error).split(".")[0])
model.fit(np.array([[1.0], [2.0], [3.0]]), np.array([2.0, 4.0, 6.0]))
print(model.coef_.round(3).tolist(), round(float(model.intercept_), 3))
try:
    model.predict(np.array([4.0]))
except ValueError as error:
    print("ValueError:", str(error).splitlines()[0])
print(model.predict(np.array([[4.0]])).round(3).tolist())
```

```text
NotFittedError: This LinearRegression instance is not fitted yet
[2.0] 0.0
ValueError: Expected 2D array, got 1D array instead:
[8.0]
```

- `fit` edilmemiş modelle tahmin `NotFittedError` verir.
- **Tek özellikli** veri bile iki boyutlu verilir: `[4.0]` bir satır mı, bir
  sütun mu belli değil, scikit-learn tahmin etmez ve durur. Doğrusu
  `[[4.0]]` (bir satır, bir sütun); bir NumPy dizisi için
  `x.reshape(-1, 1)`.

## random_state

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=300, n_features=6, n_informative=3,
                           flip_y=0.1, random_state=0)
split = train_test_split(X, y, test_size=0.25, random_state=0)
X_train, X_test, y_train, y_test = split
scores = []
for seed in [0, 1, 2]:
    forest = RandomForestClassifier(n_estimators=5, random_state=seed)
    forest.fit(X_train, y_train)
    scores.append(round(forest.score(X_test, y_test), 3))
print(X_train.shape, X_test.shape, scores)
again = RandomForestClassifier(n_estimators=5, random_state=0).fit(X_train, y_train)
print(again.score(X_test, y_test) == scores[0])
```

```text
(225, 6) (75, 6) [0.84, 0.853, 0.867]
True
```

- Rastgelelik kullanan her şey (`train_test_split`, orman, `make_classification`)
  `random_state` alır. Aynı tohum aynı sonucu verir.
- Tohum değişince skor 0,84 ile 0,867 arasında oynadı. **Tek bir tohumun
  sonucu bir modelin "gerçek" skoru değildir**; iki modeli karşılaştırırken
  bu oynama payını bilmek gerekir (doğrulama araçları bölümü).

## Veri sızıntısına ilk bakış

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=200, n_features=4, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
wrong = StandardScaler().fit(X)
right = StandardScaler().fit(X_train)
print(wrong.mean_.round(3).tolist())
print(right.mean_.round(3).tolist())
X_test_scaled = right.transform(X_test)
print(X_test_scaled.mean(axis=0).round(2).tolist())
```

```text
[0.018, 0.006, -0.014, 0.008]
[-0.109, -0.069, -0.041, -0.129]
[0.42, 0.37, 0.08, 0.34]
```

- `wrong` ortalamayı **bütün** veriden öğrendi: test satırlarını da gördü.
  Test seti artık "hiç görülmemiş veri" değil; skor gerçekte olacağından iyi
  çıkabilir. Buna **veri sızıntısı** denir.
- Doğrusu: dönüştürücü yalnızca **eğitim** verisiyle `fit` edilir, test
  verisine yalnızca `transform` uygulanır. Test verisinin ortalaması bu yüzden
  tam 0 değil; olması da gerekmez.
- Bu kuralı elle korumak zor; ileride `Pipeline` onu kendiliğinden
  uygulayacak.

## Özet

- Her nesne: kur → `fit` → `predict` / `transform`. `X` iki boyutlu.
- Hiperparametre kurucuda (`get_params`), öğrenilen değer alt çizgili
  (`coef_`). `clone` eğitilmemiş kopya.
- `NotFittedError` ve "Expected 2D array" en sık iki hata.
- Rastgelelik varsa `random_state`; tek tohumun skoruna güvenme.
- Dönüştürücüyü yalnızca eğitim verisiyle `fit` et.
