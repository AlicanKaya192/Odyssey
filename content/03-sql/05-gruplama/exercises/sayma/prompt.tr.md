Bu alıştırma `COUNT`'un üç hâlini yan yana koyuyor. Tek satır, üç sütun:

- `total_rows` — tablodaki satır sayısı
- `with_supplier` — `supplier_code` sütunu **dolu** olan satır sayısı
- `distinct_categories` — kaç **farklı** kategori olduğu

```
total_rows  with_supplier  distinct_categories
----------  -------------  -------------------
12          9              4                  
```

Üç sayının üçü de farklı ve bu bir kaza değil: aradaki 12 − 9 farkı, üç
üründe tedarikçinin kayıtlı olmadığını söylüyor.

`GROUP BY` yok — bütün tabloyu tek bir grup gibi düşünüyorsun.
