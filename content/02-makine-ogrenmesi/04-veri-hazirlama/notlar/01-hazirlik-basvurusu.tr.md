Her adım aynı kalıbı taşıyor: **eğitimde öğren, ikisine de uygula.**

## Eksik değerler

**Görmek:**

```python
print(df.isna().sum())                    # sutun basina sayi
print(df.isna().sum().sum())              # toplam
print(df[df.isna().any(axis=1)])          # eksigi olan satirlar
```

**Doldurmak (elle):**

```python
fill_value = X_train["engine"].mean()     # ya da .median()
X_train = X_train.fillna({"engine": fill_value})
X_test = X_test.fillna({"engine": fill_value})
```

**Doldurmak (sklearn):**

```python
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy="mean")
imputer.fit(X_train)
X_train = imputer.transform(X_train)
X_test = imputer.transform(X_test)
```

| `strategy` | Ne yapıyor | Ne zaman |
|---|---|---|
| `mean` | Ortalamayla doldurur | Sayısal, aykırı değer yok |
| `median` | Medyanla doldurur | Sayısal, aykırı değer var |
| `most_frequent` | En sık değerle doldurur | Kategorik |
| `constant` | Sabit bir değerle (`fill_value`) | Eksikliğin kendisi anlamlıysa |

**Atmak:**

```python
df = df.dropna()                          # eksigi olan satirlari at
df = df.dropna(subset=["engine"])         # yalnizca bu sutuna bak
df = df.drop(columns=["engine"])          # sutunun tamamini at
```

Sütunun yarısından fazlası eksikse doldurmak uydurmaya dönüşüyor; sütunu
atmak daha dürüst.

## Kategorik sütunlar

**Bulmak:**

```python
text_columns = df.select_dtypes(exclude="number").columns.tolist()
print(df["fuel"].unique())
print(df["fuel"].value_counts())
```

**pandas 3 uyarısı:** eski kaynaklardaki `df.dtypes == "object"` kontrolü
artık metin sütunlarını **bulamıyor**; `select_dtypes(exclude="number")`
kullanılıyor.

**One-hot (pandas):**

```python
encoded = pd.get_dummies(df, columns=["fuel", "gearbox"])
encoded = pd.get_dummies(df, columns=["fuel"], drop_first=True)
```

`drop_first=True` her sütundan birini atıyor: üç kategori iki sütunla
anlatılabiliyor (ikisi de 0 ise üçüncüsüdür). Doğrusal modellerde tercih
ediliyor, ağaçlarda gerekmiyor.

**One-hot (sklearn):**

```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
encoder.fit(X_train[["fuel"]])
train_encoded = encoder.transform(X_train[["fuel"]])
test_encoded = encoder.transform(X_test[["fuel"]])
```

**`get_dummies` yerine `OneHotEncoder` ne zaman:** testte eğitimde
görülmeyen bir kategori varsa. `get_dummies` iki kümede **farklı sütunlar**
üretiyor ve model çöküyor; `OneHotEncoder` eğitimdeki kategori listesini
hatırlıyor ve `handle_unknown="ignore"` ile yenilerini sessizce atıyor.

**Sıralı (ordinal) kodlama:**

```python
order = {"low": 0, "medium": 1, "high": 2}
df["level"] = df["level"].map(order)
```

Yalnızca kategoriler arasında **gerçek bir sıra** varsa.

## Ölçekleme

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

| Ölçekleyici | Sonuç | Aykırı değere |
|---|---|---|
| `StandardScaler` | Ortalama 0, standart sapma 1 | Duyarlı |
| `MinMaxScaler` | 0 ile 1 arası | Çok duyarlı |
| `RobustScaler` | Medyan ve çeyreklikler | Dayanıklı |

**`fit_transform` ne zaman kullanılır:** yalnızca eğitim kümesinde.

```python
X_train_scaled = scaler.fit_transform(X_train)   # dogru
X_test_scaled = scaler.transform(X_test)         # dogru
X_test_scaled = scaler.fit_transform(X_test)     # SIZINTI
```

Son satır ölçekleyiciyi test verisine göre yeniden öğretiyor: hem sızıntı,
hem de iki küme farklı ölçeklere gidiyor.

**Hangi model istiyor:**

| İstiyor | İstemiyor |
|---|---|
| KNN | Karar ağacı |
| SVM | Rastgele orman |
| Doğrusal modeller (düzenlileştirmeli) | Gradyan artırma |
| Kümeleme (KMeans) | Naive Bayes |
| Sinir ağları | |

## Sıra

```python
# 1. oku
df = pd.read_csv("cars.csv")

# 2. AYIR
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

# 3. eksikleri doldur (egitimden ogren)
fill_value = X_train["engine"].mean()
X_train = X_train.fillna({"engine": fill_value})
X_test = X_test.fillna({"engine": fill_value})

# 4. kategorileri kodla
# 5. olcekle (egitimde fit, ikisinde transform)
# 6. egit ve olc
```

## Sık yapılan hatalar

- **Hazırlığı ayırmadan önce yapmak.** En sık ve en sinsi hata.
- **Test kümesinde `fit_transform` çağırmak.** Sızıntı.
- **Doldurma değerini bütün veriden hesaplamak.** Sızıntı.
- **Kategoriye sırasız sıra uydurmak.** `petrol=0, diesel=1, lpg=2`.
- **`get_dummies`'i iki kümeye ayrı ayrı uygulamak.** Sütunlar tutmuyor.
- **Ölçeklemeyi hedefe (`y`) de uygulamak.** Gerekmiyor ve sonuçları
  yorumlamayı zorlaştırıyor.
- **Ağaç modelinde ölçeklemeyle zaman kaybetmek.** Zararı yok ama faydası
  da yok.
