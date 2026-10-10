## Ölçekleme

| Sınıf | Ne zaman |
|---|---|
| `StandardScaler()` | varsayılan; ortalama 0, sapma 1 |
| `RobustScaler()` | aykırı değer varsa (medyan, çeyrekler) |
| `MinMaxScaler()` | 0–1 aralığı gerekiyorsa (görüntü, sinir ağı) |
| `MaxAbsScaler()` | seyrek veri (sıfırları bozmaz) |
| — | ağaç modellerinde ölçekleme gerekmez |

## Eksik değer

| Yazım | Ne yapar |
|---|---|
| `SimpleImputer(strategy="median")` | sayılarda medyan |
| `SimpleImputer(strategy="most_frequent")` | kategoride en sık |
| `SimpleImputer(strategy="constant", fill_value=0)` | sabit |
| `add_indicator=True` | "eksikti" sütunu ekler |
| `KNNImputer(n_neighbors=5)` | benzer satırların ortalaması |

## Kategori

| Yazım | Ne zaman |
|---|---|
| `OneHotEncoder(handle_unknown="ignore")` | sırasız, az değer |
| `OrdinalEncoder(categories=[[...]])` | sıralı (beden, düzey) |
| `OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)` | bilinmeyene −1 |
| `TargetEncoder()` | çok değerli (çapraz uydurmalı) |

## Özellik üretmek

| Yazım | Ne yapar |
|---|---|
| `PolynomialFeatures(degree=2, include_bias=False)` | kareler ve etkileşimler |
| `KBinsDiscretizer(n_bins=5, encode="ordinal")` | sayıyı aralıklara böler |
| `FunctionTransformer(np.log1p)` | kendi formülün |
| `get_feature_names_out()` | yeni sütun adları |

## Hatalar

| Belirti | Sebep |
|---|---|
| `Found unknown categories ['Van']` | `handle_unknown="ignore"` yok |
| `Input X contains NaN` | model eksik değer kabul etmiyor; önce doldur |
| `could not convert string to float` | metin sütunu kodlanmadı |
| Beden S < XL < L gibi davranıyor | `OrdinalEncoder` alfabetik sıra |
| Eğitim skoru şüpheli yüksek | hedef kodlama elle yapıldı (sızıntı) |
