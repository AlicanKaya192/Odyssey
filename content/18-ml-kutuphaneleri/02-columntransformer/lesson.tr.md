# ColumnTransformer

Gerçek bir tabloda her sütun başka bir işlem ister: sayılar doldurulup
ölçeklenir, metin kategoriler one-hot kodlanır, kimlik numarası hiç modele
girmez. Bunları ayrı ayrı yapıp `np.hstack` ile yapıştırmak hem uzun hem
tehlikelidir: sütun sırası karışır, test verisinde aynı adımlar tekrar
yazılır. `ColumnTransformer` her sütun grubuna kendi dönüştürücüsünü
bağlar ve hepsini **tek bir dönüştürücü** gibi `fit` / `transform` eder.

## Bu bölümün verisi

```python
import numpy as np
import pandas as pd

homes = pd.DataFrame({
    "size": [80.0, 120.0, np.nan, 95.0, 150.0],
    "rooms": [2, 3, 3, 2, 4],
    "city": ["Izmir", "Ankara", "Izmir", "Bursa", "Ankara"],
    "heating": ["gas", "gas", "electric", None, "gas"],
    "id": [101, 102, 103, 104, 105],
})
print(homes.dtypes.astype(str).to_dict())
print(homes.isna().sum().to_dict())
```

```text
{'size': 'float64', 'rooms': 'int64', 'city': 'str', 'heating': 'str', 'id': 'int64'}
{'size': 1, 'rooms': 0, 'city': 0, 'heating': 1, 'id': 0}
```

- İki sayı sütunu (birinde eksik), iki metin sütunu (birinde eksik) ve bir
  kimlik sütunu. Bölümün diğer blokları bu `homes` tablosunu kullanıyor.

## Sütun gruplarına ayrı işlem

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numeric = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
categorical = make_pipeline(SimpleImputer(strategy="most_frequent"), onehot)
prep = ColumnTransformer([("num", numeric, ["size", "rooms"]),
                          ("cat", categorical, ["city", "heating"])])
out = prep.fit_transform(homes)
print(out.shape)
print(*prep.get_feature_names_out(), sep="\n")
print(out[2].round(2).tolist())
```

```text
(5, 7)
num__size
num__rooms
cat__city_Ankara
cat__city_Bursa
cat__city_Izmir
cat__heating_electric
cat__heating_gas
[-0.13, 0.27, 0.0, 0.0, 1.0, 1.0, 0.0]
```

- Her parça bir üçlü: **ad**, **dönüştürücü**, **sütunlar**. Sayılar için
  "doldur, sonra ölçekle" iki adımı `make_pipeline` ile tek dönüştürücü oldu
  (Pipeline'ı bir sonraki bölümde ayrıntılı göreceğiz).
- Çıktıda 7 sütun var: 2 ölçeklenmiş sayı + 3 şehir + 2 ısınma. Adlar
  `parça__sütun` biçiminde; hangi sütunun nereden geldiği okunuyor.
- Üçüncü satırda boyutu eksik ev: medyanla dolduruldu ve ölçeklendi (−0,13),
  İzmir ve elektrik sütunları 1.
- `fit` bir kez yapılır; test verisinde aynı nesneyle `transform` çağrılır.
  Her parçanın öğrendiği (medyan, ortalama, kategoriler) içinde saklanır.

## Listede olmayan sütunlar: remainder

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

drop = ColumnTransformer([("num", StandardScaler(), ["rooms"])])
keep = ColumnTransformer([("num", StandardScaler(), ["rooms"])],
                         remainder="passthrough")
print(drop.fit_transform(homes[["rooms", "id"]]).shape)
print(keep.fit_transform(homes[["rooms", "id"]]).shape)
print(keep.get_feature_names_out().tolist())
```

```text
(5, 1)
(5, 2)
['num__rooms', 'remainder__id']
```

- Varsayılan `remainder="drop"`: listede olmayan sütun **sessizce atılır**.
  Bir sütunu eklemeyi unutmak hata vermez; model o bilgiyi hiç görmez.
- `remainder="passthrough"` kalanları olduğu gibi geçirir. Kimlik numarası
  gibi modele girmemesi gereken sütun varsa bu da tehlikeli; en güvenlisi
  istenen sütunları **açıkça** listelemek.

## Türe göre seçmek ve pandas çıktısı

```python
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

numbers = make_column_selector(dtype_include="number")
texts = make_column_selector(dtype_include=object)
onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
prep = ColumnTransformer([("num", SimpleImputer(strategy="median"), numbers),
                          ("cat", onehot, texts)],
                         verbose_feature_names_out=False)
prep.set_output(transform="pandas")
out = prep.fit_transform(homes.drop(columns="heating"))
print(type(out).__name__, out.columns.tolist())
print(out.loc[2, "size"])
```

```text
DataFrame ['size', 'rooms', 'id', 'city_Ankara', 'city_Bursa', 'city_Izmir']
107.5
```

- `make_column_selector(dtype_include="number")` sütunları türlerine göre
  seçer; yeni bir sayı sütunu eklenince kodu değiştirmek gerekmez.
- Ama dikkat: **`id` de sayı**, bu yüzden özellik olarak seçildi. Kimlik
  numarası modele girerse model sıraya ya da tesadüfe göre öğrenebilir. Türe
  göre seçim kullanılıyorsa böyle sütunlar önceden atılır.
- `set_output(transform="pandas")` çıktıyı sütun adlı bir DataFrame yapar;
  `verbose_feature_names_out=False` adlardaki `parça__` önekini kaldırır.
  Ara sonuçları okumak çok kolaylaşır.

## Özet

- `ColumnTransformer([(ad, dönüştürücü, sütunlar), ...])` her sütun grubuna
  kendi işlemini uygular ve tek dönüştürücü gibi davranır.
- Birden fazla adım için parçaya `make_pipeline(...)` verilir.
- Varsayılan `remainder="drop"` listede olmayanı sessizce atar.
- `make_column_selector` türe göre seçer; kimlik gibi sayı sütunlarına dikkat.
- `get_feature_names_out` ve `set_output(transform="pandas")` sonucu
  okunur kılar.
