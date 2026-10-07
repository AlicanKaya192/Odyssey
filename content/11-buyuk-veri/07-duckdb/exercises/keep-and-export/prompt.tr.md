Kalıcı bir DuckDB veritabanı kur, içinde bir özet tablo üret ve onu
CSV'ye yaz.

**Yapman gerekenler:**

1. `make_orders(100_000)` tablosunu `orders.parquet` olarak yaz.
2. `con = duckdb.connect("shop.duckdb")` ile bağlan.
3. `orders` tablosunu Parquet dosyasından `CREATE TABLE ... AS SELECT`
   ile kur.
4. `city_summary` tablosunu kur: `city`, sipariş sayısı (`orders`) ve iki
   ondalığa yuvarlanmış ciro (`revenue`, `quantity * unit_price`
   toplamı); şehre göre sıralı.
5. `city_summary`'yi `COPY ... TO 'city_summary.csv' (HEADER)` ile yaz ve
   bağlantıyı kapat.
6. Veritabanına **yeniden** bağlan; `orders` tablosunun satır sayısını
   yazdır ve kapat.
7. `city_summary.csv` dosyasının ilk üç satırını yazdır.

**Beklenen çıktı:**

```
100000
city,orders,revenue
Adana,6936,11066810.58
Ankara,15971,25958981.76
```
