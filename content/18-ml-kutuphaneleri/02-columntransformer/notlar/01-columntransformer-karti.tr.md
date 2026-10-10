## Kurmak

| Yazım | Ne yapar |
|---|---|
| `ColumnTransformer([("ad", dönüştürücü, sütunlar), ...])` | grup başına işlem |
| `("num", make_pipeline(SimpleImputer(), StandardScaler()), [...])` | parçada birden fazla adım |
| `("drop_me", "drop", ["id"])` | sütunu açıkça at |
| `("keep", "passthrough", ["x"])` | sütunu olduğu gibi geçir |
| `remainder="drop"` (varsayılan) / `"passthrough"` | listede olmayanlar |
| `make_column_selector(dtype_include="number")` | türe göre seç |
| `make_column_selector(pattern="^price_")` | ada göre seç |
| `make_column_transformer((tr, cols), ...)` | adları kendisi verir |

## Okumak

| Yazım | Ne verir |
|---|---|
| `ct.get_feature_names_out()` | çıktı sütun adları (`parça__sütun`) |
| `verbose_feature_names_out=False` | önek olmadan |
| `ct.set_output(transform="pandas")` | DataFrame çıktı |
| `ct.named_transformers_["num"]` | eğitilmiş parça |
| `ct.transformers_` | eğitilmiş parçaların listesi |

## Hatalar

| Belirti | Sebep |
|---|---|
| Bir sütun modele hiç girmedi | listede yok, `remainder="drop"` |
| Kimlik numarası özellik oldu | türe göre seçim ya da `passthrough` |
| `Some column names are not columns of the dataframe` | sütun adı yanlış ya da yok |
| Çıktı sütunlarının sırası karışık | parçaların sırası çıktının sırası |
| Bilinmeyen kategoride hata | parçadaki `OneHotEncoder`'da `handle_unknown` yok |
