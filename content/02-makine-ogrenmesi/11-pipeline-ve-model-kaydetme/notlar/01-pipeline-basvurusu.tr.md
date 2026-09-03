## En küçük hâli

```python
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000)),
])
pipe.fit(X_train, y_train)
pipe.predict(X_test)
```

Adım adları senin seçtiğin dizeler. Son adım bir **tahminci**, öncekiler
**dönüştürücü** olmak zorunda.

Kısa yol:

```python
from sklearn.pipeline import make_pipeline
pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
```

Adları kendisi üretiyor (`standardscaler`, `logisticregression`) — hızlı
ama `GridSearchCV` anahtarları okunmaz oluyor.

## ColumnTransformer

```python
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer([
    ("num", numeric_steps, ["tenure", "monthly", "support"]),
    ("cat", text_steps, ["city", "plan"]),
])
```

| Parametre | Ne yapıyor | Varsayılan |
|---|---|---|
| `transformers` | (ad, dönüştürücü, sütunlar) üçlüleri | — |
| `remainder` | Listelenmemiş sütunlara ne olacak | `"drop"` |
| `verbose_feature_names_out` | Çıktı adlarına önek koyulsun mu | `True` |

**`remainder="drop"` varsayılan:** listelemediğin sütun **sessizce
atılıyor**. Yeni bir sütun eklendiğinde modele hiç girmiyor ve kimse fark
etmiyor. `remainder="passthrough"` onları olduğu gibi geçiriyor.

Sütun seçimini elle yazmak yerine tipe göre de yapılabiliyor:

```python
from sklearn.compose import make_column_selector

ColumnTransformer([
    ("num", numeric_steps, make_column_selector(dtype_include="number")),
    ("cat", text_steps, make_column_selector(dtype_exclude="number")),
])
```

## Doldurma

```python
from sklearn.impute import SimpleImputer

SimpleImputer(strategy="median")          # sayisal
SimpleImputer(strategy="most_frequent")   # metin
SimpleImputer(strategy="constant", fill_value="unknown")
```

`strategy`: `"mean"`, `"median"`, `"most_frequent"`, `"constant"`.

Bölüm 04'ten hatırla: medyan aykırı değerlerden ortalamadan daha az
etkileniyor.

## Kodlama

```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

OneHotEncoder(handle_unknown="ignore")
OrdinalEncoder()   # yalnizca gercekten sirali kategoriler icin
```

**`handle_unknown="ignore"` neredeyse her zaman isteniyor.** Eğitimde
görülmemiş bir değer geldiğinde varsayılan davranış hata vermek; `ignore`
o satırın bütün sütunlarını sıfır yapıyor.

`drop="first"` ilk kategoriyi atıyor — doğrusal modellerde eşdoğrusallığı
azaltıyor, ağaçlarda gereksiz.

## Adımlara ulaşmak

```python
pipe.named_steps["model"].coef_
pipe.named_steps["prepare"].get_feature_names_out()
pipe[-1]                 # son adim
pipe[:-1].transform(X)   # yalnizca on isleme
```

`get_feature_names_out()` ön işleme sonrası sütun adlarını veriyor;
katsayıları okurken tek doğru kaynak bu.

## Çapraz doğrulama

```python
cross_val_score(pipe, X_train, y_train, cv=skf, scoring="f1")
```

Pipeline verilince her adım **her katın içinde** yeniden eğitiliyor.
Sızıntı bir dikkat meselesi olmaktan çıkıyor.

Ölçüldü: 200 gürültü sütunu eklenip `SelectKBest` çapraz doğrulamanın
dışında çalıştırıldığında CV 0.780; pipeline içinde 0.716.

## GridSearchCV

```python
from sklearn.model_selection import GridSearchCV

grid = {
    "prepare__num__impute__strategy": ["median", "mean"],
    "model__C": [0.1, 1, 10],
}
search = GridSearchCV(pipe, grid, cv=skf, scoring="accuracy", n_jobs=-1)
search.fit(X_train, y_train)
```

**Anahtar biçimi:** adım adları ve parametre adı **iki alt çizgiyle**
birleşiyor. Kaç seviye olursa olsun aynı kural.

```python
search.best_params_      # en iyi ayarlar
search.best_score_       # o ayarlarin CV ortalamasi
search.best_estimator_   # butun egitim verisinde yeniden egitilmis pipeline
search.cv_results_       # her noktanin ayrintisi
search.predict(X_test)   # best_estimator_ ile tahmin
```

`refit=True` varsayılan olduğu için `best_estimator_` hazır geliyor.

Izgara büyüdüğünde `RandomizedSearchCV` aynı arayüzle rastgele bir alt
kümeyi deniyor (`n_iter` kadar).

## Kaydetmek

```python
import joblib

joblib.dump(pipe, "model.joblib")
loaded = joblib.load("model.joblib")
```

`pickle` yerine `joblib` kullanılıyor: büyük NumPy dizilerinde daha hızlı
ve daha küçük dosya üretiyor.

Sıkıştırma:

```python
joblib.dump(pipe, "model.joblib", compress=3)
```

Yavaşlatıyor ama dosyayı belirgin küçültüyor.

**Kaydedilen:** bütün adımlar, öğrenilmiş sayılar, sütun sırası.
**Kaydedilmeyen:** kütüphane sürümleri, eğitim verisi, seçtiğin eşik,
ölçtüğün skorlar. Bunlar için yanına bir metin dosyası konuyor.

**Güvenlik:** `joblib.load` dosyanın içindeki Python nesnelerini kuruyor;
güvenmediğin bir kaynaktan gelen dosya kod çalıştırabiliyor.

## Sık yapılan hatalar

- **Pipeline dışında `fit_transform` yapıp sonra `cross_val_score`
  çağırmak.** Sessiz sızıntı; ölçüldü, 6,4 puan.
- **`remainder`'ı unutmak.** Listelenmeyen sütunlar sessizce atılıyor.
- **`handle_unknown` vermemek.** Üretimde ilk beklenmedik kategoride
  çöküyor.
- **Yalnızca son adımı kaydetmek.** `joblib.dump(model, ...)` yerine
  `joblib.dump(pipe, ...)`; yoksa ön işlemenin öğrendikleri kayboluyor.
- **Tek alt çizgi yazmak.** `model_C` değil `model__C`.
- **`GridSearchCV`'nin skorunu son rapor sanmak.** `best_score_` eğitim
  tarafındaki çapraz doğrulamadan geliyor ve arama yapıldığı için
  iyimser; son rapor test kümesinde.
- **Sürüm notu bırakmamak.** Farklı bir scikit-learn sürümünde dosya
  açılmayabiliyor.
