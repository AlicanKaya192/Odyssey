Bu bölümde kullanılan her şey, aramadan bulunacak yerde.

## İçe aktarmalar

sklearn tek parça değil; her şey kendi alt paketinden geliyor.

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
```

| Alt paket | İçinde ne var |
|---|---|
| `sklearn.model_selection` | Ayırma ve doğrulama araçları |
| `sklearn.linear_model` | Doğrusal modeller |
| `sklearn.tree` | Karar ağaçları |
| `sklearn.neighbors` | KNN |
| `sklearn.metrics` | Ölçüler |
| `sklearn.preprocessing` | Ölçekleme, kodlama |

`import sklearn` tek başına işe yaramıyor — alt paket adıyla içe
aktarılıyor.

## Üç adım

```python
model = LinearRegression()          # kur
model.fit(X_train, y_train)         # ogren
prediction = model.predict(X_test)  # tahmin et
```

| Çağrı | Ne yapıyor | Ne döndürüyor |
|---|---|---|
| `Model()` | Kuruyor, henüz hiçbir şey bilmiyor | Model nesnesi |
| `fit(X, y)` | Kuralı veriden çıkarıyor | Modelin kendisi |
| `predict(X)` | Kuralı uyguluyor | Tahmin dizisi |
| `score(X, y)` | Ölçüyor (regresyonda R²) | Tek sayı |

`fit` modelin kendisini döndürdüğü için `model = LinearRegression().fit(X, y)`
tek satırda yazılabiliyor.

## Eğitimden sonra oluşan değerler

Alt çizgiyle biten her isim, `fit` çağrılmadan **yok**.

| Değer | Ne |
|---|---|
| `coef_` | Katsayılar (eğim). Tek özellikte tek sayılık dizi |
| `intercept_` | Kesişim |
| `feature_names_in_` | Eğitimde kullanılan sütun adları |
| `n_features_in_` | Kaç özellikle eğitildi |

```python
model.fit(X_train, y_train)
print(model.coef_[0], model.intercept_)
```

## `train_test_split`

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)
```

| Parametre | Ne yapıyor |
|---|---|
| `test_size` | Teste ayrılan oran (0.2 - 0.3 yaygın) |
| `train_size` | Alternatif; ikisi birden verilmiyor |
| `random_state` | Ayrımı sabitliyor, sonuç tekrarlanabilir oluyor |
| `shuffle` | Varsayılan `True`; kapatmak sırayı korur |
| `stratify` | Sınıf oranını iki tarafta da korur (sınıflandırmada) |

**Dönüş sırası sabit:** `X_train, X_test, y_train, y_test`. Karıştırmak
hata vermiyor, yanlış sonuç veriyor.

## Ölçüler

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, prediction)
mse = mean_squared_error(y_test, prediction)
rmse = mse ** 0.5
r2 = r2_score(y_test, prediction)
```

| Ölçü | Birimi | Yorumu |
|---|---|---|
| MAE | Hedefin birimi | Ortalama kaç birim yanılıyorum |
| MSE | Birimin karesi | Büyük hataları daha çok cezalandırır |
| RMSE | Hedefin birimi | MSE'nin okunabilir hâli |
| R² | Birimsiz | 1 kusursuz, 0 taban çizgi, negatif daha kötü |

**Sıra her zaman `(gerçek, tahmin)`.** Ters yazmak MAE'de fark yaratmıyor
ama R²'de yanlış sonuç veriyor.

## `X` ve `y` biçimi

```python
X = df[["area"]]            # tek ozellik  - cift parantez
X = df[["area", "age"]]     # cok ozellik
y = df["price"]             # hedef        - tek parantez
```

| Hata | Sebebi |
|---|---|
| `Expected 2D array, got 1D array` | `X` tek parantezle alınmış |
| `Found input variables with inconsistent numbers of samples` | `X` ve `y` farklı uzunlukta |
| `X has 2 features, but ... expecting 1` | Eğitim ve tahmin sütunları farklı |
| `This LinearRegression instance is not fitted yet` | `fit` çağrılmadan `predict` |

## Taban çizgi

```python
baseline = y_train.mean()
baseline_mae = mean_absolute_error(y_test, [baseline] * len(y_test))
```

sklearn'de hazırı da var:

```python
from sklearn.dummy import DummyRegressor

dummy = DummyRegressor(strategy="mean")
dummy.fit(X_train, y_train)
print(mean_absolute_error(y_test, dummy.predict(X_test)))
```

`DummyRegressor` de aynı üç adımı taşıyor — taban çizgi de bir model.

## Model değiştirmek

```python
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor

model = LinearRegression()
model = DecisionTreeRegressor(max_depth=3, random_state=42)
model = KNeighborsRegressor(n_neighbors=5)
```

Üçünde de `fit`, `predict` ve `score` aynı. Değişen yalnızca kurulum
satırı ve o modelin hiperparametreleri.
