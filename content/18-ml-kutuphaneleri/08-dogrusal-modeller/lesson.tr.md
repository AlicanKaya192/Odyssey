# Doğrusal Modeller

Doğrusal regresyonu, Ridge'i, Lasso'yu ve lojistik regresyonu ML
Algoritmaları modülünde NumPy ile sıfırdan yazdın. Bu bölüm
scikit-learn'deki hâllerinin **kullanımını** anlatıyor: katsayılar ne
zaman karşılaştırılabilir, `RidgeCV` / `LassoCV` cezayı kendisi nasıl
seçer, lojistik regresyon neden "yakınsamadı" uyarısı verir, L1 cezası bu
sürümde nasıl yazılır ve doğrusal bir model eğri bir ilişkiyi nasıl
öğrenir.

## Katsayılar ve ölçek

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(0)
area = rng.uniform(50, 200, 300)        # metrekare
rooms = rng.integers(1, 6, 300)
age = rng.uniform(0, 40, 300)            # yıl
price = 3 * area + 20 * rooms - 2 * age + rng.normal(0, 30, 300)
X = pd.DataFrame({"area": area, "rooms": rooms, "age": age})
raw = LinearRegression().fit(X, price)
print({c: round(float(v), 2) for c, v in zip(X.columns, raw.coef_)})
scaled = make_pipeline(StandardScaler(), LinearRegression()).fit(X, price)
print({c: round(float(v), 1) for c, v in zip(X.columns, scaled[-1].coef_)})
```

```text
{'area': 2.96, 'rooms': 20.21, 'age': -2.05}
{'area': 132.2, 'rooms': 28.4, 'age': -22.7}
```

- `coef_` sütun sırasıyla katsayılar, `intercept_` sabit terim. Ham
  katsayılar veriyi üreten 3, 20, −2'ye yakın: "metrekare başına 3,
  oda başına 20".
- Ham katsayıya bakıp "en önemli sütun oda" demek yanlış: oda 1–5 arası,
  metrekare 50–200 arası değişiyor. Birimleri farklı sayılar
  karşılaştırılmaz.
- Ölçeklenmiş modelde katsayı "bir standart sapmalık değişimin etkisi":
  metrekare 132,2 ile açık ara en etkili. Katsayıları **karşılaştırmak**
  istiyorsan önce ölçekle; **yorumlamak** (birim başına) istiyorsan ham
  model.

## RidgeCV: çok sütun, az satır

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.model_selection import train_test_split

X, y = make_regression(n_samples=80, n_features=60, n_informative=10,
                       noise=30, random_state=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3)
ols = LinearRegression().fit(X_train, y_train)
ridge = RidgeCV(alphas=np.logspace(-3, 3, 13)).fit(X_train, y_train)
print(round(ols.score(X_train, y_train), 3), round(ols.score(X_test, y_test), 3))
print(round(ridge.alpha_, 2), round(ridge.score(X_train, y_train), 3),
      round(ridge.score(X_test, y_test), 3))
```

```text
1.0 -5.401
3.16 0.99 0.87
```

- 60 eğitim satırı, 60 sütun: düz doğrusal regresyon eğitimi **tam**
  ezberliyor (R² 1,0) ve testte R² −5,4, yani ortalamayı tahmin etmekten
  çok daha kötü.
- `RidgeCV` verilen `alphas` arasından cezayı kendisi seçiyor (3,16) ve
  test R²'si 0,87. Eğitim skoru biraz düştü, test skoru kurtuldu.
- `RidgeCV` varsayılan olarak "birini dışarıda bırak" doğrulamasını her
  `alpha` için modeli yeniden eğitmeden, tek bir ayrıştırmadan hesaplıyor;
  `GridSearchCV(Ridge(), ...)` yazmaya gerek kalmıyor. Lojistik için
  karşılığı `LogisticRegressionCV`.

## LassoCV: tahmin mi, seçim mi?

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import Lasso, LassoCV
from sklearn.model_selection import cross_val_score

X, y, true = make_regression(n_samples=200, n_features=30, n_informative=5,
                             noise=10, coef=True, random_state=5)
lasso = LassoCV(cv=5, random_state=0).fit(X, y)
print(round(lasso.alpha_, 3), int((lasso.coef_ != 0).sum()))
print(np.flatnonzero(true).tolist())
strong = Lasso(alpha=5).fit(X, y)
print(np.flatnonzero(strong.coef_).tolist())
for alpha in [lasso.alpha_, 5]:
    print(round(cross_val_score(Lasso(alpha=alpha), X, y, cv=5).mean(), 3))
```

```text
0.257 23
[9, 18, 20, 21, 29]
[9, 18, 20, 21, 29]
0.994
0.987
```

- 30 sütunun yalnızca 5'i (`coef=True` ile gerçek katsayıları aldık:
  9, 18, 20, 21, 29) hedefi etkiliyor.
- `LassoCV` **tahmin** için en iyi cezayı seçti (0,257) ve 23 sütunu sıfır
  dışı bıraktı: gerçek 5'in yanında 18 gürültü sütunu, küçük katsayılarla.
- Daha güçlü ceza (`alpha=5`) tam olarak gerçek 5 sütunu bıraktı; tahmin
  skoru 0,994'ten 0,987'ye, çok az düştü.
- Ders: çapraz doğrulamayla seçilen Lasso iyi tahmin eder ama sütun
  **seçmek** için fazla cömerttir. Amaç az ve doğru sütunsa ceza biraz
  büyütülür.

## LogisticRegression ve yakınsama

```python
import warnings
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_wine(return_X_y=True)        # 13 ölçüm, 3 şarap türü
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    raw = LogisticRegression().fit(X, y)
print([type(w.message).__name__ for w in caught], raw.n_iter_)
pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X, y)
print(pipe[-1].n_iter_, pipe[-1].coef_.shape)
slow = LogisticRegression(max_iter=5000)
print(round(cross_val_score(slow, X, y, cv=5).mean(), 3),
      round(cross_val_score(pipe, X, y, cv=5).mean(), 3))
```

```text
['ConvergenceWarning'] [100]
[15] (3, 13)
0.961 0.983
```

- Ham veride çözücü (`lbfgs`) 100 adımlık sınıra dayandı ve
  `ConvergenceWarning` verdi: "en iyi katsayıları bulamadan durdum".
  Sebep ölçek: bir sütun 0,13–0,66 arası, `proline` 278–1680 arası.
- Ölçeklenince 15 adımda bitti. `max_iter=5000` uyarıyı susturur ama
  sorunu çözmez: ham veride doğruluk 0,961, ölçeklenmişte 0,983.
- Üç sınıfta `coef_` 3 × 13: her sınıfın kendi katsayıları var.
- `C` cezanın **tersi**: küçük `C` güçlü ceza. Ridge'deki `alpha`'nın
  tersine çalışır.

## L1 cezası: l1_ratio

```python
Xs = StandardScaler().fit_transform(X)
for C in [1, 0.1]:
    model = LogisticRegression(l1_ratio=1, solver="saga", C=C, max_iter=5000)
    model.fit(Xs, y)
    print(C, (model.coef_ != 0).sum(axis=1).tolist())
```

```text
1 [3, 8, 4]
0.1 [4, 4, 4]
```

- `l1_ratio=1` saf L1 (Lasso gibi), `0` saf L2 (varsayılan), aradaki
  değerler ikisinin karışımı (elastic net). L1'i her çözücü desteklemez;
  `saga` destekler.
- `C=1`'de sınıflar 3, 8 ve 4 sütun kullanıyor; `C=0.1`'de her biri 4.
  Ceza büyüdükçe katsayılar sıfırlanıyor.
- **Eski yazım:** internette sık görülen `penalty="l1"` bu sürümde
  `FutureWarning` veriyor ("1.8'de eskidi, 1.10'da kalkacak").
  Cezasız model için de `penalty=None` yerine `C=np.inf` yazılır.

## Eğri ilişki: PolynomialFeatures

```python
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

rng = np.random.default_rng(1)
x = rng.uniform(-3, 3, 200)
y = 2 * np.sin(x) + rng.normal(0, 0.3, 200)
X = x.reshape(-1, 1)
cv = KFold(5, shuffle=True, random_state=0)
for degree in [1, 3, 5]:
    model = make_pipeline(PolynomialFeatures(degree), StandardScaler(),
                          Ridge(alpha=1e-3))
    print(degree, round(cross_val_score(model, X, y, cv=cv).mean(), 3))
names = PolynomialFeatures(2).fit(np.zeros((1, 3))).get_feature_names_out()
print(names.tolist())
print(PolynomialFeatures(3).fit(np.zeros((1, 20))).n_output_features_)
```

```text
1 0.641
3 0.963
5 0.966
['1', 'x0', 'x1', 'x2', 'x0^2', 'x0 x1', 'x0 x2', 'x1^2', 'x1 x2', 'x2^2']
1771
```

- İlişki sinüs; düz çizgi R² 0,641'de kalıyor. `PolynomialFeatures(3)`
  `x`'in yanına `x²` ve `x³` sütunlarını ekliyor; model hâlâ **doğrusal**
  (yeni sütunlarda), ama eğri çiziyor: 0,963.
- Birden çok sütunda çarpımlar da ekleniyor (`x0 x1`). 3 sütun 2. derecede
  10 sütun, 20 sütun 3. derecede 1771 sütun: hızla patlar. Bu yüzden arkasına
  Ridge gibi cezalı model konur.

## Özet

- Katsayıları karşılaştırmak için ölçekle; birim başına yorum için ham
  model.
- Çok sütun / az satırda düz regresyon ezberler; `RidgeCV` / `LassoCV` cezayı
  kendisi seçer.
- `LassoCV` tahmin için iyi, sütun seçmek için cömert.
- `ConvergenceWarning` çoğu zaman ölçek eksikliğidir; `max_iter` ile
  susturma.
- L1 için `l1_ratio=1` ve `solver="saga"`; `penalty=` eskidi.
