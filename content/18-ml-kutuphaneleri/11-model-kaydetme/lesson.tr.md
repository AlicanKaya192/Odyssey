# Model Kaydetme

`joblib.dump` ve `joblib.load`'u Makine Öğrenmesi patikasında gördün:
pipeline'ın tamamı tek dosyaya giriyor. Orada sözle geçen üç uyarı vardı:
dosya sürümü, sütunları ve kaynağın güvenilirliğini bilmiyor. Bu bölüm
üçünü de **çalıştırarak** gösteriyor ve her birine karşı ne yapılacağını
anlatıyor: modelin yanına bilgi koymak, girdiyi denetlemek, dosyayı
sıkıştırmak, eski sürüm dosyasını yakalamak.

## Modelle birlikte bilgi kaydet

```python
import joblib
import pandas as pd
import sklearn
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=500, n_features=4, n_informative=3,
                           n_redundant=0, random_state=2)
X = pd.DataFrame(X, columns=["age", "income", "visits", "score"])
model = make_pipeline(StandardScaler(), LogisticRegression()).fit(X, y)
bundle = {"model": model, "sklearn": sklearn.__version__,
          "columns": list(X.columns), "threshold": 0.3, "cv_auc": 0.91}
joblib.dump(bundle, "churn.joblib")
loaded = joblib.load("churn.joblib")
print(sorted(loaded), loaded["sklearn"])
print(loaded["model"].feature_names_in_.tolist())
```

```text
['columns', 'cv_auc', 'model', 'sklearn', 'threshold'] 1.9.1
['age', 'income', 'visits', 'score']
```

- `joblib.dump` yalnızca modeli değil, herhangi bir Python nesnesini
  kaydeder. Bir sözlükle modelin **yanına** şunlar konur: eğitildiği
  scikit-learn sürümü, beklediği sütunlar, seçilen karar eşiği, ölçülen
  skor. Altı ay sonra dosyayı açan kişi (belki sen) bunları başka yerde
  aramaz.
- DataFrame ile eğitilen model sütun adlarını kendisi de tutar:
  `feature_names_in_`.

## Girdiyi denetle

```python
import warnings

new = X.head(3)
print(loaded["model"].predict_proba(new)[:, 1].round(3).tolist())
shuffled = new[["income", "age", "visits", "score"]]
for bad in [shuffled, new.drop(columns="score")]:
    try:
        loaded["model"].predict_proba(bad)
    except ValueError as err:
        print(str(err).splitlines()[1])
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    as_array = loaded["model"].predict_proba(new.to_numpy())[:, 1]
print(as_array.round(3).tolist(), str(caught[0].message)[:40])
```

```text
[0.991, 0.47, 0.143]
Feature names must be in the same order as they were in fit.
Feature names seen at fit time, yet now missing:
[0.991, 0.47, 0.143] X does not have valid feature names, but
```

- Sütunların **sırası** değişince ya da biri **eksik** olunca model hata
  veriyor. Bu iyi: yanlış tahmin yerine durmak.
- Ama aynı veriyi NumPy dizisi olarak verince yalnızca bir **uyarı**
  ("geçerli sütun adı yok") çıkıyor ve tahmin yapılıyor. Dizide ad yok;
  sütunlar yanlış sırada olsaydı model bunu bilemez, sessizce yanlış sayı
  üretirdi.
- Kural: modele her zaman sütun adlı DataFrame ver ve önce kendi
  listenle sırala: `new[bundle["columns"]]`.

## Dosya boyu: compress

```python
import os
from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(n_estimators=200, random_state=0).fit(X, y)
for level in [0, 3, 9]:
    joblib.dump(forest, f"forest{level}.joblib", compress=level)
    print(level, os.path.getsize(f"forest{level}.joblib") // 1024)
again = joblib.load("forest3.joblib")
print(bool((again.predict(X) == forest.predict(X)).all()))
```

```text
0 1254
3 261
9 216
True
```

- 200 ağaçlı orman sıkıştırmasız 1254 KB. `compress=3` ile 261 KB, beşte
  birinden az; `9` biraz daha küçük (216 KB). Kazancın çoğu ilk
  seviyelerde.
- Sıkıştırma kayıpsız: yüklenen orman aynı tahminleri veriyor.
- Küçük modellerde gerekmez (bu verideki lojistik pipeline 2 KB'tan
  küçük); ağaç topluluklarında ve büyük modellerde önemli.

## Güvenmediğin dosyayı açma

```python
class Trap:
    def __reduce__(self):
        return (print, ("loading this file ran code",))


joblib.dump(Trap(), "trap.joblib")
result = joblib.load("trap.joblib")
print(result)
```

```text
loading this file ran code
None
```

- `joblib` (ve altındaki `pickle`) bir nesneyi kaydederken "beni nasıl
  geri kuracaksın" bilgisini de yazar. `__reduce__` bunu bir **fonksiyon
  çağrısı** olarak verebiliyor; yükleme o çağrıyı yapar.
- Burada zararsız bir `print` çalıştı. Aynı yere dosya silen ya da internete
  bağlanan bir fonksiyon da yazılabilir; `load` bunu hiç sormadan çalıştırır.
- Kural: yalnızca kendi ürettiğin ya da kaynağına güvendiğin model
  dosyasını yükle. İnternetten indirilen bir `.joblib` / `.pkl` dosyası,
  çalıştırılabilir bir program gibi düşünülür.

## Eski sürümün dosyası

```python
import pickle
from sklearn.exceptions import InconsistentVersionWarning

data = pickle.dumps(LogisticRegression().fit(X, y))
old_file = data.replace(sklearn.__version__.encode(), b"1.2.2")   # eski kayıt gibi
with warnings.catch_warnings():
    warnings.simplefilter("error", InconsistentVersionWarning)
    try:
        pickle.loads(old_file)
    except InconsistentVersionWarning as warning:
        print(warning.estimator_name, warning.original_sklearn_version,
              warning.current_sklearn_version)
```

```text
LogisticRegression 1.2.2 1.9.1
```

- Her model nesnesi hangi scikit-learn sürümüyle kaydedildiğini içinde
  taşır. Burada o bilgiyi elle "1.2.2" yaparak eski bir dosyayı taklit
  ettik.
- Farklı sürümde yükleme normalde yalnızca bir uyarı verir
  (`InconsistentVersionWarning`) ve devam eder; model çalışıyor gibi görünür
  ama sonuçlar değişmiş olabilir.
- `simplefilter("error", ...)` uyarıyı hataya çevirir: yükleme durur ve
  uyarının içinden hangi model, hangi sürümler okunur. Sunucuda çalışan bir
  model için güvenli olan budur; çözüm modeli o sürümde yeniden eğitmek ya
  da ortamı eğitildiği sürüme sabitlemektir.

## Özet

- Modeli bir sözlükte sürüm, sütunlar, eşik ve skorla birlikte kaydet.
- Tahminden önce sütunları kendi listenle sırala; NumPy dizisi verme.
- Büyük modellerde `compress=3`.
- Güvenmediğin model dosyasını yükleme: yüklemek kod çalıştırmaktır.
- Sürüm farkını `InconsistentVersionWarning` ile yakala, sessiz geçme.
