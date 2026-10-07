20 000 siparişlik tabloda bellekte en çok yer tutan üç sütunu bul.

**Yapman gerekenler:**

1. `write_orders_csv("orders.csv", 20_000)` ile dosyayı yaz, `df`'ye oku.
2. `df.memory_usage(deep=True)` ile sütun başına baytı al; `Index` satırını
   çıkar.
3. Büyükten küçüğe sırala ve ilk üç sütunu döngüyle yazdır: her satırda
   sütunun adı ve **kilobayt** olarak boyutu (`/ 1024`, bir ondalık).
4. Son satıra tablonun toplamını kilobayt olarak (bir ondalık) yazdır.

**Beklenen çıktı:**

```
order_time 527.3
city 282.2
category 279.3
1963.5
```

İlk üç sütunun üçü de metin.
