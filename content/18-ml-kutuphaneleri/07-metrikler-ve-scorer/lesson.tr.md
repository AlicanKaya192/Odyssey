# Metrikler ve Scorer

MAE, F1, AUC gibi ölçüleri Makine Öğrenmesi patikasında tanıdın. Bu bölüm
onların scikit-learn'deki **kullanımına** bakıyor: `scoring=` yazınca ne
oluyor, neden bazı skorlar eksi çıkıyor, çok sınıfta F1 nasıl
ortalanıyor, AUC'ye neden olasılık verilmeli, kendi ölçünü (örneğin bir
hatanın **maliyetini**) nasıl araçlara verirsin ve karar eşiğini nasıl
doğru yerde seçersin.

## scoring= ve eksi işareti

```python
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import get_scorer_names
from sklearn.model_selection import cross_val_score

print(len(get_scorer_names()))
X, y = make_regression(n_samples=200, n_features=4, noise=20, random_state=1)
scores = cross_val_score(LinearRegression(), X, y, cv=5,
                         scoring="neg_mean_absolute_error")
print(scores.round(1))
print(round(-scores.mean(), 2))
```

```text
58
[-12.8 -14.  -15.3 -14.1 -14.9]
14.22
```

- `scoring=` bir **ad** alır; `get_scorer_names()` hepsini listeler (bu
  sürümde 58). Aynı ad `cross_val_score`, `cross_validate`,
  `GridSearchCV`, `learning_curve` hepsinde geçer.
- scikit-learn'ün kuralı: **büyük skor daha iyi**. Arama "en büyüğü" seçer.
  Hata ölçülerinde küçük daha iyi olduğu için eksiyle çevrilmiş hâlleri var:
  `neg_mean_absolute_error`, `neg_root_mean_squared_error`, `neg_log_loss`.
- Eksi işaret raporda gösterilmez: ortalamanın eksisini al. MAE 14,22.

## Çok sınıfta ortalama

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=8, n_informative=5,
                           n_classes=3, weights=[0.7, 0.2, 0.1], random_state=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3,
                                                    stratify=y)
pred = LogisticRegression().fit(X_train, y_train).predict(X_test)
for avg in [None, "macro", "weighted", "micro"]:
    print(avg, np.round(f1_score(y_test, pred, average=avg), 3))
print(classification_report(y_test, pred, digits=3))
```

```text
None [0.886 0.488 0.341]
macro 0.572
weighted 0.752
micro 0.776
              precision    recall  f1-score   support

           0      0.827     0.954     0.886       175
           1      0.625     0.400     0.488        50
           2      0.438     0.280     0.341        25

    accuracy                          0.776       250
   macro avg      0.630     0.545     0.572       250
weighted avg      0.747     0.776     0.752       250
```

- İkiden fazla sınıfta her sınıfın ayrı bir F1'i var (`average=None`):
  çoğunluk sınıfı 0,886, en küçük sınıf 0,341.
- `macro`: sınıfların düz ortalaması (0,572). Küçük sınıf büyük kadar
  sayılır; küçük sınıfı kaçırmak bu sayıyı düşürür.
- `weighted`: sınıf büyüklüğüyle ağırlıklı (0,752). Çoğunluk sınıfı
  baskın; küçük sınıfların kötülüğünü gizler.
- `micro`: bütün tahminler tek havuzda (0,776); tek etiketli çok sınıfta
  doğrulukla aynı (`accuracy 0.776`).
- Scorer adı olarak: `"f1_macro"`, `"f1_weighted"`, `"recall_macro"`.
  `classification_report(..., output_dict=True)` aynı tabloyu sözlük
  olarak verir.

## AUC olasılık ister

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=2000, n_features=8, n_informative=4,
                           weights=[0.95], flip_y=0.02, random_state=7)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=7,
                                                    stratify=y)
model = LogisticRegression().fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
pred = model.predict(X_test)
auc_pred = roc_auc_score(y_test, pred)
auc_proba = roc_auc_score(y_test, proba)
print(round(auc_pred, 3), round(auc_proba, 3))
print(round(average_precision_score(y_test, proba), 3), round(y_test.mean(), 3))
```

```text
0.599 0.776
0.433 0.06
```

- AUC, modelin pozitifleri negatiflerin **önüne dizme** başarısıdır; bunun
  için sıralanabilir bir puan gerekir. `predict` yalnızca 0/1 veriyor:
  AUC 0,599 çıktı. Aynı modelin olasılığıyla 0,776.
- `roc_auc_score(y, pred)` hata vermez, sessizce yanlış sayı verir. AUC'ye
  her zaman `predict_proba(X)[:, 1]` (ya da `decision_function`) verilir.
  `scoring="roc_auc"` bunu kendisi yapar.
- Pozitifler %6 iken `average_precision` (precision–recall eğrisinin alanı)
  daha dürüst: rastgele bir model 0,06 alır, bu model 0,433. AUC'nin 0,5'lik
  tabanı nadir sınıfta iyi görünmeyi kolaylaştırır.

## make_scorer: kendi ölçün

Bu veride bir pozitifi **kaçırmak** (yanlış negatif) 10 birim, boşuna alarm
(yanlış pozitif) 1 birim tutsun. Doğruluk ya da F1 bunu bilmez; maliyeti
kendimiz yazarız:

```python
from sklearn.metrics import confusion_matrix, make_scorer
from sklearn.model_selection import cross_val_score


def cost(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return fp * 1 + fn * 10


scorer = make_scorer(cost, greater_is_better=False)
print(cost(y_test, pred), scorer(model, X_test, y_test))
for weight in [None, "balanced"]:
    m = LogisticRegression(class_weight=weight)
    scores = cross_val_score(m, X_train, y_train, cv=5, scoring=scorer)
    print(weight, round(-scores.mean(), 1))
```

```text
241 -241
None 113.6
balanced 94.8
```

- Ölçü fonksiyonu `(y_true, y_pred)` alıp bir sayı döndürür.
  `make_scorer` onu `scorer(model, X, y)` biçimine çevirir; artık her
  `scoring=` yerine verilebilir.
- `greater_is_better=False`: maliyet küçük olmalı, scorer onu **eksiyle**
  döndürür (−241). Arama yine "en büyüğü" seçer, yani en az maliyetliyi.
- Bu ölçüyle iki model karşılaştırılabilir: `class_weight="balanced"` kat
  başına ortalama maliyeti 113,6'dan 94,8'e indirdi.

## Karar eşiğini doğru yerde seçmek

`predict` olasılığı 0,5'te keser. Maliyetler eşit değilse 0,5 doğru eşik
değildir:

```python
import numpy as np
from sklearn.model_selection import TunedThresholdClassifierCV

for t in [0.5, 0.2, 0.1, 0.05]:
    print(t, cost(y_test, (proba >= t).astype(int)))
tuned = TunedThresholdClassifierCV(LogisticRegression(), scoring=scorer, cv=5)
tuned.fit(X_train, y_train)
print(round(tuned.best_threshold_, 3), cost(y_test, tuned.predict(X_test)))
```

```text
0.5 241
0.2 202
0.1 161
0.05 181
0.181 207
```

- Eşik düştükçe kaçırılan pozitif azalıyor, boşuna alarm artıyor. Test
  verisinde en ucuzu 0,1 (161). Ama eşiği **test verisine bakarak**
  seçmek, test verisini eğitime katmaktır; o 161 iyimser.
- `TunedThresholdClassifierCV` eşiği **eğitim verisinde**, çapraz
  doğrulamayla ve verilen scorer'a göre seçer: 0,181. Test maliyeti
  241'den 207'ye indi. Bu dürüst sayıdır.
- Eşiği elle sabitlemek için `FixedThresholdClassifier(model,
  threshold=0.2)`; ikisi de `predict`'i değiştirir, `predict_proba` aynı
  kalır.

## Aramada birden çok ölçü

```python
from sklearn.model_selection import GridSearchCV

search = GridSearchCV(LogisticRegression(), {"C": [0.01, 0.1, 1, 10]}, cv=5,
                      scoring={"auc": "roc_auc", "ap": "average_precision"},
                      refit="ap").fit(X_train, y_train)
print(search.best_params_, round(search.best_score_, 3))
print(sorted(k for k in search.cv_results_ if k.startswith("mean_test")))
```

```text
{'C': 10} 0.599
['mean_test_ap', 'mean_test_auc']
```

- `scoring=` bir sözlük olabilir: her ölçü ayrı sütun olarak
  `cv_results_`'a girer (`mean_test_auc`, `mean_test_ap`).
- Birden çok ölçüde arama hangisine göre "en iyi"yi seçeceğini bilemez:
  `refit="ap"` ile söylenir. `best_score_` o ölçünün değeridir.

## Özet

- `scoring=` ad alır; büyük daha iyi, hatalar `neg_` ile eksi.
- Çok sınıfta `average`: `macro` küçük sınıfı korur, `weighted` gizler.
- AUC ve average precision olasılık ister; `predict` verme.
- İşin kendi maliyeti varsa `make_scorer(..., greater_is_better=False)`.
- Eşik test verisinde değil, `TunedThresholdClassifierCV` ile eğitimde
  seçilir.
