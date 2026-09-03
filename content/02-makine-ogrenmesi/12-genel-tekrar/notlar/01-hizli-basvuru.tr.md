## İskelet

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("data.csv")
X = df.drop(columns="target")
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

numeric = ["a", "b"]
text = ["c", "d"]

preprocessor = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), numeric),
    ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                      ("encode", OneHotEncoder(handle_unknown="ignore"))]), text),
])

pipe = Pipeline([("prepare", preprocessor), ("model", model)])
folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipe, X_train, y_train, cv=folds)

pipe.fit(X_train, y_train)
print(accuracy_score(y_test, pipe.predict(X_test)))
```

`stratify=y` yalnızca sınıflandırmada; regresyonda `KFold` kullanılıyor.

## Taban çizgi

```python
# siniflandirma: en sik sinif
baseline = accuracy_score(y_test, [y_train.mode()[0]] * len(y_test))

# regresyon: egitim ortalamasi
baseline = mean_absolute_error(y_test, [y_train.mean()] * len(y_test))
```

Bu satır her projede yazılıyor. Yoksa hiçbir skor okunamıyor.

## Modeller

```python
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import (RandomForestClassifier, RandomForestRegressor,
                              GradientBoostingClassifier)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
```

| Model | Ne zaman | Ölçekleme | Ana ayar |
|---|---|---|---|
| `LinearRegression` | İlişki doğrusalsa | Gerekmiyor | — |
| `LogisticRegression` | İkili sınıflandırma, hızlı taban | Yararlı | `C`, `class_weight` |
| `KNeighbors*` | Küçük veri, yerel örüntü | **Zorunlu** | `n_neighbors` |
| `DecisionTree*` | Yorumlanabilirlik şart | Gerekmiyor | `max_depth` |
| `RandomForest*` | Genel amaçlı, kararlı | Gerekmiyor | `n_estimators` |
| `GradientBoosting*` | Yanlılık düşürmek | Gerekmiyor | `learning_rate` |
| `KMeans` | Etiket yok, grup aranıyor | **Zorunlu** | `n_clusters` |
| `PCA` | Boyut indirgeme, çizim | **Zorunlu** | `n_components` |

## Metrikler

```python
# regresyon
from sklearn.metrics import (mean_absolute_error, root_mean_squared_error,
                             r2_score)

# siniflandirma
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix,
                             classification_report, roc_auc_score,
                             average_precision_score)

# kumeleme
from sklearn.metrics import silhouette_score, adjusted_rand_score
```

| Metrik | Ne söylüyor | Taban çizgisi |
|---|---|---|
| MAE | Ortalama mutlak hata, birim aynı | Ortalamanın MAE'si |
| RMSE | Büyük hataları cezalandırıyor | Ortalamanın RMSE'si |
| R² | Varyansın ne kadarı açıklandı | 0 |
| Doğruluk | Doğru bilinen oranı | En sık sınıfın oranı |
| Precision | Pozitif dediklerinin ne kadarı doğru | — |
| Recall | Gerçek pozitiflerin ne kadarı yakalandı | — |
| F1 | İkisinin harmonik ortalaması | — |
| ROC AUC | Sıralama yeteneği | 0.5 |
| Ortalama precision | PR eğrisi altındaki alan | **Pozitif oranı** |
| Silüet | Kümeler ne kadar derli toplu | Gürültüdeki değeri |

Son sütun sık atlanıyor ve en çok yanlış okumaya yol açan yer.

## Çapraz doğrulama

```python
scores = cross_val_score(pipe, X_train, y_train, cv=folds,
                         scoring="average_precision")
print(round(float(scores.mean()), 3), round(float(scores.std()), 3))
```

**Ortalama tek başına okunmuyor; yayılım da yazılıyor.** İki modelin
ortalaması arasındaki fark yayılımlardan küçükse fark yok demektir.

Yaygın `scoring` değerleri: `"accuracy"`, `"precision"`, `"recall"`,
`"f1"`, `"roc_auc"`, `"average_precision"`, `"r2"`,
`"neg_mean_absolute_error"`.

## Ayar araması

```python
from sklearn.model_selection import GridSearchCV

grid = {
    "prepare__num__impute__strategy": ["median", "mean"],
    "model__C": [0.1, 1, 10],
}
search = GridSearchCV(pipe, grid, cv=folds, scoring="accuracy")
search.fit(X_train, y_train)
print(search.best_params_, round(float(search.best_score_), 3))
```

Adım adları ve parametre **iki alt çizgiyle** birleşiyor. `best_score_`
son rapor değil — o eğitim tarafından geliyor ve iyimser.

## Dengesiz veri

```python
model = LogisticRegression(max_iter=1000, class_weight="balanced")

probability = pipe.predict_proba(X_test)[:, 1]
prediction = (probability >= 0.1).astype(int)
```

`predict()` her zaman 0.5 kullanıyor. Eşik bir iş kararı ve **eğitim
tarafında** seçiliyor.

## Kaydetmek

```python
import joblib
joblib.dump(pipe, "model.joblib")
loaded = joblib.load("model.joblib")
```

Modelin **tamamı** kaydediliyor. Yanına kütüphane sürümlerini, eşiği ve
ölçtüğün skorları yazan bir metin dosyası konuyor.

## Değişmeyen dört kural

1. **Taban çizgiyi ölç.** Yoksa hiçbir skor okunamıyor.
2. **Önce ayır, sonra dokun.** Pipeline bunu garanti ediyor.
3. **Test kümesine bir kez bak.** İkinci bakış skoru iyimser yapıyor.
4. **Tek sayıya güvenme.** Yayılıma, karışıklık matrisine, taban çizgiye
   birlikte bak.
