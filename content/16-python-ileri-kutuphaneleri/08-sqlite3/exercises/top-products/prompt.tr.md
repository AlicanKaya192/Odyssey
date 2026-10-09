`top_products(items, n)` fonksiyonunu yaz: bellekte bir veritabanı
açsın, `row_factory` olarak `sqlite3.Row` versin, `products (name, price)`
tablosunu kursun ve `items` listesini `executemany` ile eklesin. Fiyata göre
büyükten küçüğe ilk `n` ürünün **adlarını** liste olarak döndürsün; adı
`row["name"]` ile alsın.

**Beklenen çıktı:**

```
['bag', 'book']
```
