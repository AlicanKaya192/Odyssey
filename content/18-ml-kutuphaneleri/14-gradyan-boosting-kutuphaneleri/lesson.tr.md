# Gradyan Boosting Kütüphaneleri

Gradyan artırmanın (boosting) fikrini ML Algoritmaları modülünde yazdın:
her yeni ağaç öncekilerin hatasını düzeltir. Tablo verisinde en güçlü
modeller çoğu zaman bu ailedendir. Bu bölüm iki hızlı uygulamasını
anlatıyor: scikit-learn'ün `HistGradientBoostingClassifier`'ı ve ayrı bir
paket olan **LightGBM**. Konular hız, eksik değer ve kategorik sütunlar,
erken durdurma ve iki tür özellik önemi.

## HistGradientBoosting: hız

```python
import time
from sklearn.datasets import make_classification
from sklearn.ensemble import (GradientBoostingClassifier,
                              HistGradientBoostingClassifier)
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=20000, n_features=20, n_informative=8,
                           flip_y=0.05, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
seconds = {}
for model in [GradientBoostingClassifier(random_state=0),
              HistGradientBoostingClassifier(random_state=0)]:
    start = time.perf_counter()
    model.fit(X_train, y_train)
    seconds[type(model).__name__] = time.perf_counter() - start
    print(type(model).__name__, round(model.score(X_test, y_test), 3))
print(model.n_iter_, model.early_stopping)
old, new = seconds.values()
print(old > 10 * new)
```

```text
GradientBoostingClassifier 0.943
HistGradientBoostingClassifier 0.955
86 auto
True
```

- `HistGradientBoostingClassifier` her sütunu önce en fazla 255 kutuya
  (histogram) böler ve kesim noktasını kutular arasında arar. Bütün
  değerleri tek tek denemekten çok daha hızlı: bu bilgisayarda 15 000
  satırda eski sınıf yaklaşık 10 saniye, yenisi yarım saniyenin altında
  (son satır: 10 kattan fazla).
- Doğruluk da daha iyi (0,955 ile 0,943). 10 000 satırın üstünde eski
  `GradientBoostingClassifier`'ı seçmek için sebep yok.
- `early_stopping="auto"` varsayılan: veri 10 000 satırdan büyükse
  kendisi bir doğrulama parçası ayırır ve iyileşme durunca ağaç eklemeyi
  bırakır. Burada 100 ağaç yerine 86'da durdu (`n_iter_`).

## Eksik değer ve kategorik sütun

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(2)
names = [f"c{i}" for i in range(30)]
effect = dict(zip(names, rng.normal(0, 1, 30)))
city = rng.choice(names, 6000)
x1 = rng.normal(0, 1, 6000)
chance = 1 / (1 + np.exp(-(1.5 * pd.Series(city).map(effect) + x1)))
target = (rng.random(6000) < chance).astype(int)
df = pd.DataFrame({"city": pd.Categorical(city), "x1": x1})
df.loc[rng.random(6000) < 0.1, "x1"] = np.nan          # %10 eksik
d_train, d_test, t_train, t_test = train_test_split(df, target, random_state=2)
native = HistGradientBoostingClassifier(categorical_features="from_dtype",
                                        random_state=0)
native.fit(d_train, t_train)
print(native.is_categorical_.tolist(), round(native.score(d_test, t_test), 3))
codes = HistGradientBoostingClassifier(categorical_features=None, random_state=0)
codes.fit(d_train.assign(city=d_train.city.cat.codes), t_train)
as_codes = d_test.assign(city=d_test.city.cat.codes)
print(round(codes.score(as_codes, t_test), 3))
```

```text
[True, False] 0.739
0.746
```

- 30 şehirli bir kategorik sütun ve %10'u eksik bir sayı sütunu. Model
  ikisini de **ön işleme olmadan** aldı: `NaN` için ayrı yön öğreniyor,
  `category` türündeki sütunu `categorical_features="from_dtype"` ile
  kategorik tanıyor (`is_categorical_`: `[True, False]`).
- Kategorik bölmede ağaç "c3, c17, c25 bir yana, gerisi öbür yana" gibi
  kümeler kurabilir. Şehirleri sıra numarasına çevirip (`cat.codes`) sayı
  gibi vermek de bu veride neredeyse aynı skoru verdi (0,746 ile 0,739):
  yerli desteğin kazancı burada doğruluk değil, kolaylık. Hangisinin iyi
  olduğu veriye göre değişir; ölçmeden üstün sayılmaz.

## LightGBM ve erken durdurma

```python
import lightgbm as lgb
from lightgbm import LGBMClassifier
from sklearn.metrics import log_loss

X, y = make_classification(n_samples=3000, n_features=20, n_informative=6,
                           flip_y=0.2, random_state=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3)
X_fit, X_val, y_fit, y_val = train_test_split(X_train, y_train, test_size=0.25,
                                              random_state=3)
settings = dict(n_estimators=2000, learning_rate=0.05, random_state=0, verbose=-1)
stopped = LGBMClassifier(**settings)
stopped.fit(X_fit, y_fit, eval_X=X_val, eval_y=y_val,
            callbacks=[lgb.early_stopping(50, verbose=False)])
full = LGBMClassifier(**settings).fit(X_fit, y_fit)
for name, model in [("stopped", stopped), ("full", full)]:
    proba = model.predict_proba(X_test)
    accuracy = model.score(X_test, y_test)
    print(name, round(accuracy, 3), round(log_loss(y_test, proba), 3))
print(stopped.best_iteration_)
```

```text
stopped 0.828 0.439
full 0.817 1.195
57
```

- LightGBM'in scikit-learn arayüzü tanıdık: `LGBMClassifier(...).fit(X, y)`,
  `predict`, `predict_proba`, pipeline'a ve `GridSearchCV`'ye girer.
  `verbose=-1` eğitim mesajlarını susturur.
- Veride etiketlerin %20'si gürültü. 2000 ağaçlık model gürültüyü de
  öğreniyor: test doğruluğu 0,817, log kaybı **1,195** (olasılıkları aşırı
  emin ve yanlış).
- Erken durdurma: eğitim verisinden ayrı bir **doğrulama** parçası
  (`eval_X`, `eval_y`) her ağaçtan sonra ölçülür; 50 ağaç boyunca
  iyileşmezse durur. 57. ağaçta durdu: doğruluk 0,828, log kaybı 0,439.
- Doğrulama parçası testten **ayrı**: test verisiyle durdurmak, testi
  eğitime katmaktır.
- **Sürüm notu:** eski öğreticilerde `eval_set=[(X_val, y_val)]` yazar; bu
  sürümde eskidi (`LGBMDeprecationWarning`), yerine `eval_X` ve `eval_y`.

## İki tür önem

```python
X, y = make_classification(n_samples=20000, n_features=20, n_informative=8,
                           flip_y=0.05, random_state=1)
model = LGBMClassifier(random_state=0, verbose=-1).fit(X, y)
split = model.feature_importances_
gain = model.booster_.feature_importance(importance_type="gain")
for i in [4, 5, 1]:
    print(i, int(split[i]), round(gain[i] / gain.sum(), 3))
```

```text
4 254 0.316
5 414 0.121
1 73 0.003
```

- LightGBM'in `feature_importances_`'ı varsayılan olarak **bölme sayısı**:
  sütun ağaçlarda kaç kez kullanıldı. `gain` ise o bölmelerin kayıbı ne
  kadar azalttığı.
- İkisi farklı sıralıyor: 5. sütun en çok bölmede (414) ama kazancın
  %12,1'ini sağlıyor; 4. sütun daha az bölmede (254) ama kazancın %31,6'sı
  onun. 1. sütun bir gürültü sütunu: 73 kez kullanılmış, kazancı %0,3.
- "Hangi sütun önemli?" sorusu için `gain` daha anlamlı; ikisi de eğitim
  verisinden gelir. Görülmemiş veride önem için permütasyon önemi (Modeli
  Açıklamak bölümü).

## Özet

- 10 000 satırın üstünde `HistGradientBoostingClassifier` ya da LightGBM;
  eski `GradientBoostingClassifier` yavaş.
- İkisi de `NaN`'ı ve `category` sütununu ön işlemesiz alır.
- Erken durdurma ayrı bir doğrulama parçasıyla; LightGBM'de `eval_X`,
  `eval_y` ve `lgb.early_stopping`.
- LightGBM önemi varsayılan olarak bölme sayısı; `gain` daha anlamlı.
