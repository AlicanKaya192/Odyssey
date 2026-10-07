Bir CSV dosyasını belleğe almadan, kategori başına sipariş sayısını ve
ortalama fiyatı DuckDB ile bul.

**Yapman gerekenler:**

1. `write_orders_csv("orders.csv", 200_000)` ile dosyayı yaz.
2. DuckDB ile `'orders.csv'` üstünde: `category`, sipariş sayısı ve iki
   ondalığa yuvarlanmış ortalama `unit_price`; sipariş sayısına göre
   büyükten küçüğe.
3. Sonucu `fetchall()` ile al ve her satırı üç değer yan yana olacak
   şekilde yazdır.

**Beklenen çıktı:**

```
clothing 44401 551.89
books 43837 191.58
home 39756 477.68
electronics 28040 2557.45
toys 24143 340.94
sports 19823 808.52
```
