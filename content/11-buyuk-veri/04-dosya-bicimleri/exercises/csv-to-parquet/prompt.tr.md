Bir CSV dosyasını türleriyle birlikte Parquet'ye taşı ve hiçbir şeyin
kaybolmadığını doğrula.

**Yapman gerekenler:**

1. `write_orders_csv("orders.csv", 300_000)` ile CSV'yi yaz.
2. CSV'yi şu türlerle `df` olarak oku: `city`, `category`, `payment`
   `"category"`, `quantity` `"int8"`, `order_time` tarih (`parse_dates`).
3. `df`'yi `zstd` sıkıştırmayla `orders.parquet` olarak yaz.
4. CSV ve Parquet boyutlarını MB olarak (bir ondalık) aynı satıra, altına
   CSV / Parquet oranını (bir ondalık) yazdır.
5. Parquet'yi `back` olarak geri oku. Aynı satıra iki şey yazdır:
   `back.equals(df)` ve türlerin aynı olup olmadığı
   (`(back.dtypes == df.dtypes).all()`).

**Beklenen çıktı:**

```
18.0 4.7
3.9
True True
```

`True True`: değerler de türler de birebir aynı; bundan sonra bu dosyayı her
okuyuşta türleri yeniden vermek gerekmiyor.
