# Hiperparametre Arama

`C` kaç olmalı, kaç sütun seçilmeli, ağaç ne kadar derin olmalı? Bu
hiperparametreleri veriden öğrenen bir formül yok; denenip çapraz
doğrulamayla karşılaştırılırlar. `GridSearchCV` verilen bütün
kombinasyonları, `RandomizedSearchCV` rastgele bir kısmını dener. Bu bölüm
ikisini, sonuç tablosunu okumayı ve aramanın kendisinin **iyimser**
olduğunu, yani en iyi skorun gerçek başarıdan yüksek çıktığını gösteriyor.

## GridSearchCV ve pipeline

```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=600, n_features=20, n_informative=5,
                           flip_y=0.05, random_state=10)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
pipe = make_pipeline(StandardScaler(), SelectKBest(f_classif), LogisticRegression())
grid = {"selectkbest__k": [3, 5, 10, 20], "logisticregression__C": [0.01, 0.1, 1.0]}
search = GridSearchCV(pipe, grid, cv=5).fit(X_train, y_train)
print(search.best_params_)
print(round(search.best_score_, 3), round(search.score(X_test, y_test), 3))
print(len(search.cv_results_["params"]))
```

```text
{'logisticregression__C': 1.0, 'selectkbest__k': 5}
0.853 0.867
12
```

- Izgara bir sözlük: anahtar `adım__ayar`, değer denenecek liste. 4 × 3 = 12
  kombinasyon, her biri 5 katlı çapraz doğrulama: 60 eğitim.
- Aramanın tamamı **eğitim** verisinde yapılır; test verisi en sonda bir kez
  kullanılır. `search.score(X_test, y_test)` en iyi ayarla bütün eğitim
  verisine yeniden eğitilmiş (`refit=True`, varsayılan) modelle hesaplanır.
- `best_params_` en iyi kombinasyon, `best_score_` onun çapraz doğrulama
  ortalaması. Eğitilmiş en iyi model `search.best_estimator_`.

## Sonuç tablosunu okumak

```python
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split

X, y = make_classification(n_samples=600, n_features=20, n_informative=5,
                           flip_y=0.05, random_state=10)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
grid = {"C": [0.001, 0.01, 0.1, 1.0, 10.0]}
search = GridSearchCV(LogisticRegression(), grid, cv=5).fit(X_train, y_train)
cols = ["param_C", "mean_test_score", "std_test_score", "rank_test_score"]
print(pd.DataFrame(search.cv_results_)[cols].round(3).to_string(index=False))
```

```text
 param_C  mean_test_score  std_test_score  rank_test_score
   0.001            0.824           0.041                5
   0.010            0.844           0.043                1
   0.100            0.842           0.040                3
   1.000            0.842           0.037                3
  10.000            0.844           0.035                1
```

- `cv_results_` her kombinasyonun ortalama skorunu, katlar arası sapmasını
  ve sırasını verir. DataFrame'e çevirince okunur.
- Asıl ders bu tabloda: 0,01'den 10'a kadar bütün `C`'lerin ortalaması
  0,842–0,844 arasında, sapma ise 0,04. Farklar **gürültüden küçük**. "En
  iyi" `C` seçildi ama başka bir tohumla başka biri seçilebilirdi.
- Böyle düz bir tabloda en basit (en çok düzenlileştiren) ayarı seçmek
  daha güvenlidir; yalnızca 0,001 belirgin şekilde kötü.

## RandomizedSearchCV

```python
from scipy.stats import loguniform, randint
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split

X, y = make_classification(n_samples=600, n_features=20, n_informative=5,
                           flip_y=0.05, random_state=10)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
space = {"n_estimators": randint(20, 200), "max_depth": randint(2, 12),
         "min_samples_leaf": randint(1, 20), "max_features": loguniform(0.1, 1.0)}
search = RandomizedSearchCV(RandomForestClassifier(random_state=10), space,
                            n_iter=15, cv=3, random_state=10).fit(X_train, y_train)
print(sorted(search.best_params_), round(search.best_score_, 3))
print(round(search.score(X_test, y_test), 3))
```

```text
['max_depth', 'max_features', 'min_samples_leaf', 'n_estimators'] 0.862
0.927
```

- Dört ayarın her biri için 5 değer bile 625 kombinasyon eder. Rastgele
  arama bunların yerine `n_iter` (15) rastgele kombinasyon dener.
- Liste yerine **dağılım** verilebilir: `randint(2, 12)` tam sayı,
  `loguniform(0.1, 1.0)` oranların ve `C` gibi ölçeği katlanarak değişen
  ayarların doğru aralığı (0,1 ile 0,2 arasındaki fark, 0,9 ile 1,0 arasındakiyle
  aynı önemde).
- Ayarların çoğu sonucu az etkiler; rastgele arama aynı bütçeyle önemli
  ayarın daha çok farklı değerini dener. Çok ayarlı modellerde ızgaradan
  verimlidir.

## Aramanın iyimserliği

```python
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(11)
X = rng.normal(size=(120, 30))
y = rng.integers(0, 2, 120)
pipe = make_pipeline(SelectKBest(f_classif), LogisticRegression())
grid = {"selectkbest__k": list(range(1, 31)),
        "logisticregression__C": np.logspace(-3, 2, 10).tolist()}
search = GridSearchCV(pipe, grid, cv=5).fit(X, y)
print(len(search.cv_results_["params"]), round(search.best_score_, 3))
outer = cross_val_score(GridSearchCV(pipe, grid, cv=5), X, y, cv=5)
print(round(outer.mean(), 3))
```

```text
300 0.642
0.517
```

- Veri yine **tamamen rastgele**. 300 kombinasyon denendi ve en iyisinin
  çapraz doğrulama skoru 0,642 çıktı. Seçim doğru, sızıntı yok; ama 300 aday
  arasından **en şanslısını** seçtik. `best_score_` bu yüzden iyimserdir.
- Dürüst ölçü **iç içe çapraz doğrulama**: aramanın kendisi bir dış çapraz
  doğrulamanın içinde çalışır; her dış katın test verisi aramayı hiç
  görmez. Sonuç 0,517: şansa eşit, yani gerçek.
- Aday sayısı arttıkça iyimserlik büyür. Raporda `best_score_` değil, ayrı
  tutulmuş test skoru ya da iç içe doğrulama yazılır.

## Özet

- `GridSearchCV(pipe, {"adım__ayar": [...]}, cv=5)` bütün kombinasyonlar;
  `RandomizedSearchCV(..., n_iter=)` dağılımlardan rastgele örnek.
- Arama eğitim verisinde, test bir kez ve en sonda; `refit` en iyi ayarla
  yeniden eğitir.
- `cv_results_`'ta ortalama kadar **sapmaya** bak: farklar gürültüden küçükse
  basit olanı seç.
- `best_score_` iyimserdir; dürüst tahmin için ayrı test ya da iç içe
  çapraz doğrulama.
