# Metin için Pipeline

Şimdiye kadar vektörleştiriciyi ve modeli ayrı ayrı `fit` ettik ve her
seferinde "vektörleştiriciyi yalnızca eğitim verisiyle kur" kuralını elle
hatırladık. **Pipeline** ikisini tek bir nesnede birleştirir: ham metin girer,
tahmin çıkar. Bu yalnızca kolaylık değil; çapraz doğrulamada ve parametre
aramada sızıntıyı kendiliğinden önler, ve modeli kaydedip kullanırken
vektörleştiriciyi unutmayı imkânsız kılar. Bu bölüm metin için Pipeline
kurmayı, çapraz doğrulamayı, vektörleştiricinin ve modelin ayarlarını
birlikte aramayı ve farklı özellikleri birleştirmeyi anlatıyor. ML
Kütüphaneleri'nde gördüğün Pipeline'ın metindeki kullanımı.

## Pipeline kurmak

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
pipe = Pipeline([("tfidf", TfidfVectorizer()),
                 ("model", LogisticRegression(max_iter=1000))])
pipe.fit(X_train, y_train)
print(round(pipe.score(X_test, y_test), 3))
print(pipe.predict(["not good at all", "love it"]).tolist())
```

```text
0.88
['positive', 'positive']
```

- `Pipeline` adımları sırayla bağlar: her adımın bir adı (`"tfidf"`,
  `"model"`) ve bir nesnesi var. `fit` vektörleştiriciyi `fit_transform`,
  modeli `fit` ediyor; `predict` vektörleştiriciyi yalnızca `transform`
  ediyor.
- Girdi artık **ham metin**: `pipe.predict(["not good at all"])`. Tahmin
  yaparken vektörleştiriciyi ayrıca çağırmayı unutmak mümkün değil.
- Sonuç 09'daki ayrı ayrı kurulan modelle aynı: %88. Ama dikkat: bu model
  "not good at all"u **olumlu** buldu. Tek kelimelik lojistik regresyon
  "good"un ağırlığına güvendi; 08'deki Naive Bayes ise olumsuz demişti. Tek
  örnek bir şey kanıtlamaz, ama kelime çiftlerinin neden önemli olduğunu
  hatırlatır.

## Çapraz doğrulama

Tek bir eğitim/test bölmesi şanslı ya da şanssız olabilir. **Çapraz
doğrulama** (cross-validation) eğitim verisini k parçaya böler; her seferinde
bir parçayı doğrulama, kalanı eğitim için kullanır ve k skorun ortalamasını
verir.

```python
from sklearn.model_selection import cross_val_score

cv = cross_val_score(pipe, X_train, y_train, cv=5, scoring="f1_macro")
print(cv.round(3).tolist(), round(cv.mean(), 3))
leaky_X = TfidfVectorizer().fit_transform(X_train)
leaky = cross_val_score(LogisticRegression(max_iter=1000), leaky_X, y_train,
                        cv=5, scoring="f1_macro")
print(round(leaky.mean(), 3))
```

```text
[0.874, 0.896, 0.857, 0.842, 0.89] 0.872
0.874
```

- Beş katın macro F1'i 0,842 ile 0,896 arasında oynuyor: tek bir bölmenin
  skoru ±0,03 yanılabilir. Ortalama 0,872.
- Pipeline'ı `cross_val_score`'a verince vektörleştirici **her katta**
  yalnızca o katın eğitim kısmıyla yeniden `fit` ediliyor.
- İkinci deneme sızıntılı yol: vektörleştirici bütün eğitim verisiyle bir kez
  kuruldu, sonra çapraz doğrulandı. Doğrulama kısmının kelimeleri ve IDF'i
  her katta modele sızdı. Bu veride fark küçük (0,874'e 0,872), çünkü
  dağarcık küçük ve kelimeler her yerde geçiyor. Nadir kelimelerin ve
  `min_df` gibi eşiklerin önemli olduğu gerçek veride fark büyür. Pipeline
  ile bu soru hiç doğmaz.

## Parametre arama

Vektörleştiricinin ayarları (n-gram, `sublinear_tf`) ve modelin `C` değeri
birlikte aranabilir. Parametrenin adı `adım__parametre` biçiminde yazılır:

```python
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV

grid = GridSearchCV(pipe, {
    "tfidf__ngram_range": [(1, 1), (1, 2)],
    "tfidf__sublinear_tf": [False, True],
    "model__C": [1, 10],
}, cv=5, scoring="f1_macro")
grid.fit(X_train, y_train)
print(grid.best_params_)
print(round(grid.best_score_, 3))
print(round(f1_score(y_test, grid.predict(X_test), average="macro"), 3))
```

```text
{'model__C': 10, 'tfidf__ngram_range': (1, 2), 'tfidf__sublinear_tf': True}
0.888
0.868
```

- 2 × 2 × 2 = 8 ayar, her biri 5 katta: 40 model eğitildi. En iyisi kelime
  çiftleri, `sublinear_tf=True` ve `C=10`.
- **Dikkat:** `best_score_` (0,888) test skorundan (0,868) yüksek. Sekiz
  ayarın en iyisini seçmek, doğrulama skorunu şanslı katlara uydurmak
  demek; seçilen ayarın skoru iyimserdir. Gerçek performansı her zaman
  aramada hiç kullanılmamış test verisinde ölç (ML Kütüphaneleri'ndeki
  iyimser `best_score_` dersi).
- `grid` en iyi ayarla bütün eğitim verisinde yeniden eğitilmiş bir Pipeline
  gibi kullanılabilir: `grid.predict(...)`.

## Özellikleri birleştirmek

`FeatureUnion` aynı metinden farklı özellikler üretip yan yana koyar:
kelime n-gram'ları ve harf n-gram'ları.

```python
from sklearn.pipeline import FeatureUnion
from sklearn.svm import LinearSVC

words = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
                  ("model", LinearSVC())])
both = Pipeline([
    ("features", FeatureUnion([
        ("words", TfidfVectorizer(ngram_range=(1, 2))),
        ("chars", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))),
    ])),
    ("model", LinearSVC()),
])
for name, model in [("words", words), ("words+chars", both)]:
    model.fit(X_train, y_train)
    macro = f1_score(y_test, model.predict(X_test), average="macro")
    print(name, round(model.score(X_test, y_test), 3), round(macro, 3))
```

```text
words 0.916 0.874
words+chars 0.912 0.863
```

Harf n-gram'ları eklemek bu veride **yardım etmedi** (%91,6'ya %91,2). Harf
n-gram'ları yazım hatası ve ek çeşitliliği çok olan metinde parlar;
yorumlarımızın dağarcığı küçük ve kelimeler zaten tekrar ediyor. Her ekleme
işe yaramaz; birleştirdiğin her özelliği ölç.

## Metin ve başka bir sütun

Elimizde metnin yanında başka bilgiler de olabilir: yorumun hangi ürüne ait
olduğu. `ColumnTransformer` her sütuna kendi dönüştürücüsünü uygular:

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

products = [r["product"] for r in reviews]
frame = pd.DataFrame({"text": texts, "product": products})
F_train, F_test, f_train, f_test = train_test_split(
    frame, labels, test_size=0.25, random_state=0, stratify=labels)
mixed = Pipeline([
    ("columns", ColumnTransformer([
        ("text", TfidfVectorizer(ngram_range=(1, 2)), "text"),
        ("product", OneHotEncoder(handle_unknown="ignore"), ["product"]),
    ])),
    ("model", LinearSVC()),
])
mixed.fit(F_train, f_train)
print(round(mixed.score(F_test, f_test), 3))
```

```text
0.914
```

- Metin sütunu `TfidfVectorizer`'a **tek sütun adı** olarak (`"text"`)
  verilir: vektörleştirici bir metin listesi bekler, tablo değil. Kategorik
  sütun ise liste olarak (`["product"]`).
- Ürün türü bilgisi bir şey katmadı (%91,4): bu veride ürünün duyguyla
  ilgisi yok. Gerçek veride (örneğin bazı ürünlerin daha çok şikâyet
  alması) yardım edebilir.

## Özet

- Pipeline vektörleştiriciyi ve modeli bağlar: ham metin girer, tahmin
  çıkar; vektörleştiriciyi unutmak imkânsızlaşır.
- `cross_val_score(pipe, ...)` vektörleştiriciyi her katta yeniden kurar;
  sızıntı kendiliğinden önlenir.
- `GridSearchCV` vektörleştiricinin ve modelin ayarlarını birlikte arar
  (`tfidf__ngram_range`, `model__C`); `best_score_` iyimserdir, son ölçümü
  testte yap.
- `FeatureUnion` aynı metinden farklı özellikleri, `ColumnTransformer` farklı
  sütunları birleştirir. Bu veride ikisi de kazandırmadı: her eklemeyi ölç.
