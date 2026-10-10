# Ön İşleme

Modeller sayı ister, eksiksiz sayı ister ve çoğu benzer ölçekte sayı ister.
Gerçek veri ise eksik değerli, metin kategorili ve birimleri birbirinden çok
farklı sütunlarla gelir. `sklearn.preprocessing` ve `sklearn.impute` bu
farkı kapatan dönüştürücüleri verir. Hepsi önceki bölümün sözleşmesine uyar:
eğitim verisiyle `fit`, her yerde `transform`. Bu bölüm ölçekleyicileri,
eksik değer doldurmayı, kategori kodlamayı ve yeni özellik üretmeyi; her
birinin **yanlış seçildiğinde** ne yaptığıyla birlikte anlatıyor.

## Üç ölçekleyici, bir aykırı değer

```python
import numpy as np
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

income = np.array([[30.0], [35.0], [40.0], [45.0], [500.0]])
for scaler in [StandardScaler(), MinMaxScaler(), RobustScaler()]:
    out = scaler.fit_transform(income).ravel().round(2)
    print(type(scaler).__name__, out.tolist())
```

```text
StandardScaler [-0.54, -0.51, -0.49, -0.46, 2.0]
MinMaxScaler [0.0, 0.01, 0.02, 0.03, 1.0]
RobustScaler [-1.0, -0.5, 0.0, 0.5, 46.0]
```

| Ölçekleyici | Ne yapar | Aykırı değerle |
|---|---|---|
| `StandardScaler` | ortalamayı çıkar, sapmaya böl | aykırı ortalamayı ve sapmayı çeker; dört normal değer −0,54…−0,46'ya sıkıştı |
| `MinMaxScaler` | en küçüğü 0, en büyüğü 1 yap | dört değer 0–0,03 arasına ezildi |
| `RobustScaler` | medyanı çıkar, çeyrekler arası farka böl | normal değerler −1…0,5'e açıldı, aykırı 46'da tek başına |

- Aykırı değerli veride `RobustScaler` geri kalan değerlerin farklarını
  korur. Aykırı değer yoksa `StandardScaler` varsayılan seçimdir.
- Uzaklığa ya da eğime dayanan modeller (KNN, SVM, düzenlileştirilmiş
  doğrusal modeller, sinir ağları) ölçeğe duyarlıdır; **ağaç modelleri
  değildir**, onlarda ölçekleme gereksizdir.

## Eksik değer doldurmak

```python
import numpy as np
from sklearn.impute import SimpleImputer

X = np.array([[1.0, 7.0], [np.nan, 8.0], [3.0, np.nan], [100.0, 9.0]])
for strategy in ["mean", "median"]:
    imp = SimpleImputer(strategy=strategy)
    filled = imp.fit_transform(X)[:, 0].round(2).tolist()
    print(strategy, filled, imp.statistics_.round(2).tolist())
flagged = SimpleImputer(strategy="median", add_indicator=True).fit_transform(X)
print(flagged.shape, flagged[:, 2:].astype(int).tolist())
```

```text
mean [1.0, 34.67, 3.0, 100.0] [34.67, 8.0]
median [1.0, 3.0, 3.0, 100.0] [3.0, 8.0]
(4, 4) [[0, 0], [1, 0], [0, 1], [0, 0]]
```

- `SimpleImputer` eksik değeri sütunun bir istatistiğiyle doldurur;
  istatistik `statistics_`'te, **eğitim verisinden** öğrenilmiştir.
- İlk sütunda 100 gibi bir aykırı değer var: ortalama boşluğu 34,67 ile
  doldurdu (hiçbir gerçek değere benzemiyor), medyan 3 ile.
- `add_indicator=True` her eksikli sütun için "burası eksikti" sütunu ekler
  (son iki sütun). Bir değerin **eksik olması** bilgi taşıyabilir (müşteri
  geliri yazmadıysa); doldurunca o bilgi kaybolmasın.
- Sabit değerle doldurmak için `strategy="constant", fill_value=0`; kategorik
  sütunda `strategy="most_frequent"`.

## Kategoriler: OneHotEncoder

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

train = pd.DataFrame({"city": ["Izmir", "Ankara", "Izmir", "Bursa"]})
enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
print(enc.fit_transform(train).astype(int).tolist())
print(enc.get_feature_names_out().tolist())
print(enc.transform(pd.DataFrame({"city": ["Van"]})).astype(int).tolist())
strict = OneHotEncoder().fit(train)
try:
    strict.transform(pd.DataFrame({"city": ["Van"]}))
except ValueError as error:
    print("ValueError:", str(error).split(" in column")[0])
```

```text
[[0, 0, 1], [1, 0, 0], [0, 0, 1], [0, 1, 0]]
['city_Ankara', 'city_Bursa', 'city_Izmir']
[[0, 0, 0]]
ValueError: Found unknown categories ['Van']
```

- Her kategori bir 0/1 sütunu olur. Sıra **yoktur**: Ankara < İzmir gibi
  sahte bir ilişki kurulmaz.
- `get_feature_names_out` yeni sütunların adlarını verir; model sonuçlarını
  okurken gerekir.
- Eğitimde görülmemiş bir kategori (Van) üretimde mutlaka gelir. Varsayılan
  ayar hata verip durur; `handle_unknown="ignore"` onu bütün sütunları 0
  olan bir satıra çevirir.
- `sparse_output=False` sonucu sıradan dizi yapar; çok kategoride varsayılan
  seyrek matris bellek kazandırır.

## Sıralı kategoriler: OrdinalEncoder

```python
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

sizes = pd.DataFrame({"size": ["M", "S", "XL", "L"]})
auto = OrdinalEncoder().fit(sizes)
print(auto.categories_[0].tolist(), auto.transform(sizes).ravel().tolist())
ordered = OrdinalEncoder(categories=[["S", "M", "L", "XL"]]).fit(sizes)
print(ordered.transform(sizes).ravel().tolist())
```

```text
['L', 'M', 'S', 'XL'] [1.0, 2.0, 3.0, 0.0]
[1.0, 0.0, 3.0, 2.0]
```

- `OrdinalEncoder` her kategoriye tek bir sayı verir. Kendi başına sırayı
  **alfabetik** seçer: L=0, M=1, S=2, XL=3. Beden için anlamsız; doğrusal bir
  model "S, XL'den küçük ama L'den büyük" diye öğrenir.
- `categories=[[...]]` ile sırayı sen verirsin: S=0, M=1, L=2, XL=3.
- Sırası olmayan kategoride (şehir) `OneHotEncoder`; sıralı olanda
  (beden, eğitim düzeyi) sırası verilmiş `OrdinalEncoder`. Ağaç modelleri
  sırasız kategoride de sıralı kodla iyi çalışabilir.

## Yeni özellik üretmek

```python
import numpy as np
from sklearn.preprocessing import PolynomialFeatures

X = np.array([[2.0, 3.0]])
poly = PolynomialFeatures(degree=2, include_bias=False).fit(X)
print(poly.get_feature_names_out(["a", "b"]).tolist(), poly.transform(X).tolist())
```

```text
['a', 'b', 'a^2', 'a b', 'b^2'] [[2.0, 3.0, 4.0, 6.0, 9.0]]
```

- `PolynomialFeatures` kareleri ve **etkileşimleri** (`a b`) ekler: doğrusal
  model eğri ve "iki özellik birlikte" etkilerini öğrenebilir.
- Sütun sayısı hızla büyür: 10 özellik ikinci derecede 65 sütun olur.
  Düzenlileştirmeyle birlikte kullanılır (doğrusal modeller bölümü).
- Sayıyı aralıklara bölmek için `KBinsDiscretizer`, kendi formülün için
  `FunctionTransformer(np.log1p)` gibi araçlar da aynı arayüzü kullanır.

## Özet

- Ölçekleme: aykırı yoksa `StandardScaler`, varsa `RobustScaler`;
  ağaçlarda gereksiz.
- Eksik değer: `SimpleImputer` (aykırıda medyan), eksikliğin kendisi için
  `add_indicator=True`.
- Sırasız kategori `OneHotEncoder(handle_unknown="ignore")`, sıralı kategori
  `OrdinalEncoder(categories=[[...]])`.
- Hepsi eğitim verisiyle `fit` edilir; öğrendikleri `statistics_`,
  `categories_`, `mean_` gibi alanlarda.
