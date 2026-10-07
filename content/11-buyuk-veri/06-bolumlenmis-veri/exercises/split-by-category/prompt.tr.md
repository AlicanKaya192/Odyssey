Siparişleri kategoriye göre klasörlere ayır.

**Yapman gerekenler:**

1. `make_orders(100_000)` ile `df` tablosunu kur.
2. `df.groupby("category")` ile gez. Her kategori için
   `by_category/category=<ad>` klasörünü aç
   (`mkdir(parents=True, exist_ok=True)`) ve o kategorinin satırlarını,
   `category` sütunu **çıkarılmış** olarak, `part-0.parquet` adıyla yaz
   (`index=False`).
3. `by_category` içindeki klasörlerin adlarını sıralı olarak, her biri ayrı
   satırda yazdır.
4. Son satıra klasör sayısını yazdır.

**Beklenen çıktı:**

```
category=books
category=clothing
category=electronics
category=home
category=sports
category=toys
6
```
