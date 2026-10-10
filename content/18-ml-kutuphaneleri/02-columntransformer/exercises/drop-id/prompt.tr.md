`keep_all_but_id(rows)` bir `ColumnTransformer` kursun: `id` sütunu açıkça
atılsın (`("drop_id", "drop", ["id"])`), geri kalan her şey olduğu gibi geçsin
(`remainder="passthrough"`, `verbose_feature_names_out=False`). Çıktı sütun
adlarını döndürsün. Başlangıç kodu her şeyi geçiriyor; `id` de çıktıda.

**Beklenen çıktı:**

```
['size', 'city']
```
