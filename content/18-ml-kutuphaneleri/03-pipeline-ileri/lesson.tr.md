# Pipeline ve Kendi Dönüştürücün

`Pipeline` hazırlık adımlarını ve modeli tek bir nesnede arka arkaya bağlar.
Önceki bölümlerde onu kısa yoldan kullandık; bu bölüm üç şeyi gösteriyor:
adımlara ve ayarlarına nasıl ulaşılır, pipeline **neden** sızıntıyı önler
(rastgele veride %88 "başarıyı" ölçerek göreceğiz) ve scikit-learn'de hazır
olmayan bir adımı kendi dönüştürücün olarak nasıl yazarsın.

## Adımlar ve ayarları

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler

pipe = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression(C=1.0))])
print(list(pipe.named_steps))
auto = make_pipeline(StandardScaler(), LogisticRegression())
print(list(auto.named_steps))
pipe.set_params(model__C=0.1)
print(pipe.get_params()["model__C"], pipe["model"].C)
print(type(pipe[:-1]).__name__, len(pipe[:-1]))
```

```text
['scale', 'model']
['standardscaler', 'logisticregression']
0.1 0.1
Pipeline 1
```

- `Pipeline([(ad, adım), ...])` adları sen verirsin; `make_pipeline` sınıf
  adının küçük harfini kullanır.
- İç adımın ayarı **`adım__ayar`** biçiminde yazılır (iki alt çizgi):
  `model__C`. Hiperparametre araması bütün pipeline üzerinde bu adlarla
  çalışır.
- `pipe["model"]` adıyla, `pipe[:-1]` dilimle ulaşır; dilim de bir
  pipeline'dır (modelsiz hazırlık kısmı). Hazırlanmış veriyi görmek için
  `pipe[:-1].transform(X)`.
- Son adım dışındaki bütün adımlar dönüştürücü olmalı; son adım model ya da
  dönüştürücü olabilir.

## Pipeline neden sızıntıyı önler?

```python
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(6)
X = rng.normal(size=(100, 5000))
y = rng.integers(0, 2, 100)
X_selected = SelectKBest(f_classif, k=20).fit_transform(X, y)
wrong = cross_val_score(LogisticRegression(), X_selected, y, cv=5).mean()
pipe = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression())
right = cross_val_score(pipe, X, y, cv=5).mean()
print(round(wrong, 2), round(right, 2))
```

```text
0.88 0.58
```

- Veri **tamamen rastgele**: 5000 gürültü sütunu, rastgele hedef. Gerçek
  başarı %50 civarı olmalı.
- Yanlış yol: hedefle en ilişkili 20 sütunu bütün veriden seçip **sonra**
  çapraz doğrulama. Seçim test katlarının cevaplarını da gördü; 5000 rastgele
  sütunun içinde tesadüfen hedefle uyuşanlar seçildi. Sonuç: %88, tamamen
  sahte.
- Doğru yol: seçim pipeline'ın içinde. Çapraz doğrulama her katta pipeline'ı
  `clone`'layıp yalnızca o katın eğitim verisiyle `fit` eder; seçim test
  katını hiç görmez. Sonuç: %58, şansa yakın.
- Kural: **veriden bir şey öğrenen her adım** (ölçekleme, doldurma, seçme,
  kodlama) pipeline'ın içinde olmalı.

## Kendi dönüştürücün

```python
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class Clipper(BaseEstimator, TransformerMixin):
    def __init__(self, low=0.01, high=0.99):
        self.low = low
        self.high = high

    def fit(self, X, y=None):
        X = np.asarray(X, dtype=float)
        self.lower_ = np.quantile(X, self.low, axis=0)
        self.upper_ = np.quantile(X, self.high, axis=0)
        return self

    def transform(self, X):
        check_is_fitted(self)
        return np.clip(np.asarray(X, dtype=float), self.lower_, self.upper_)


X = np.array([[1.0], [2.0], [3.0], [4.0], [100.0]])
clip = Clipper(low=0.0, high=0.75)
print(clip.fit_transform(X).ravel().tolist(), clip.upper_.tolist())
print(clip.get_params())
```

```text
[1.0, 2.0, 3.0, 4.0, 4.0] [4.0]
{'high': 0.75, 'low': 0.0}
```

- Aykırı değerleri sınırlayan (kırpan) bir adım scikit-learn'de hazır yok;
  sözleşmeye uyan bir sınıf yazınca pipeline'a girer.
- **`__init__` yalnızca ayarları saklar**, başka iş yapmaz; parametre adları
  nitelik adlarıyla aynı olmalı. `BaseEstimator` `get_params` / `set_params`'ı
  bu kurala bakarak kendisi yazar (`clone` ve arama bunu kullanır).
- **`fit` öğrenir** (sınırları eğitim verisinden), sonuçları alt çizgili
  niteliklere koyar ve `self` döndürür.
- **`transform` uygular**; `check_is_fitted` eğitilmemişse anlaşılır hata
  verir. `TransformerMixin` `fit_transform`'u kendisi ekler.
- 100 değeri, eğitim verisinin %75 yüzdeliğine (4) kırpıldı.

## Kısa yol: FunctionTransformer

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

X = np.array([[1.0], [10.0], [100.0], [1000.0]])
y = np.array([1.0, 2.0, 3.0, 4.0])
plain = LinearRegression().fit(X, y)
logged = make_pipeline(FunctionTransformer(np.log10), LinearRegression()).fit(X, y)
print(round(plain.score(X, y), 3), round(logged.score(X, y), 3))
print(logged.predict([[10_000.0]]).round(2).tolist())
```

```text
0.679 1.0
[5.0]
```

- Adım veriden hiçbir şey **öğrenmiyorsa** (logaritma, oran, sütun seçmek)
  sınıf yazmaya gerek yok: `FunctionTransformer(fonksiyon)`.
- Logaritmik ilişkide düz doğrusal model R² 0,679 aldı; log alınınca
  ilişki tam doğru oldu (1,0) ve 10 000 için tahmin 5.
- Öğrenen bir adımı (`np.mean` ile ortalama çıkarmak gibi) fonksiyonla
  yazmak sızıntıya yol açar: fonksiyon her çağrıda **o anki** verinin
  ortalamasını alır, eğitimdekini değil.

## Özet

- `Pipeline` / `make_pipeline`; iç ayar `adım__ayar`; `pipe["ad"]`,
  `pipe[:-1]`.
- Veriden öğrenen her adım pipeline'ın içinde; yoksa çapraz doğrulama sahte
  başarı gösterir.
- Kendi dönüştürücün: `BaseEstimator` + `TransformerMixin`, `__init__` yalnızca
  ayar, `fit` öğrenir ve `self` döner, `transform` uygular.
- Öğrenmeyen adım için `FunctionTransformer`.
