Aynı CSV'nin türlerini DuckDB'ye ve pandas'a sor.

**Yapman gerekenler:**

1. `write_orders_csv("orders.csv", 50_000)` ile dosyayı yaz.
2. DuckDB ile `DESCRIBE SELECT * FROM 'orders.csv'` sonucundan
   `column_name` ve `column_type` sütunlarını al (`fetchall()`); her
   satıra sütun adını ve türünü yazdır.
3. Son satıra pandas'ın aynı dosyadaki `order_time` sütunu için seçtiği
   türü yazdır.

**Beklenen çıktı:**

```
order_id BIGINT
order_time TIMESTAMP
customer_id BIGINT
city VARCHAR
category VARCHAR
quantity BIGINT
unit_price DOUBLE
payment VARCHAR
str
```

DuckDB tarihi tanıdı; pandas metin olarak bıraktı.
