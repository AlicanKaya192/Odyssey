`df`'de `category` türünde bir `city` sütunu ve eksikli bir `x1` sütunu var.
`category_model(min_leaf)` iki sütunu da **ön işlemesiz** kullansın
(`categorical_features="from_dtype"`) ve `[is_categorical_, test_skoru]`
döndürsün (skor 3 basamak). Başlangıç kodu şehri hiç kullanmıyor.

**Beklenen çıktı:**

```
[[True, False], 0.739]
```
