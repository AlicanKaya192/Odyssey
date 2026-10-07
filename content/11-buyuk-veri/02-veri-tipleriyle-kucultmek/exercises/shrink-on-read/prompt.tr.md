Aynı dosyayı iki kez oku: bir kez türleri pandas'a bırakarak, bir kez
türleri kendin vererek. Belleği karşılaştır.

**Yapman gerekenler:**

1. `write_orders_csv("orders.csv", 200_000)` ile dosyayı yaz.
2. `plain = pd.read_csv("orders.csv")`.
3. `typed` tablosunu `read_csv` ile şu türlerle oku:
   - `order_id`, `customer_id`: `"int32"`
   - `quantity`: `"int8"`
   - `unit_price`: `"float32"`
   - `city`, `category`, `payment`: `"category"`
   - `order_time`: `parse_dates` ile tarih
4. İki tablonun belleğini MB olarak, bir ondalığa yuvarlayıp aynı satıra
   yazdır.
5. Küçülme oranını (`plain / typed`) bir ondalığa yuvarlayıp yazdır.
6. `typed` tablosunda `order_time` ve `city` sütunlarının türünü aynı
   satıra yazdır.

**Beklenen çıktı:**

```
19.2 4.6
4.2
datetime64[us] category
```
