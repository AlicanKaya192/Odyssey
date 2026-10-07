Spark DataFrame ile kartla ödenen siparişlerin kategori raporunu çıkar ve
aynı sonucu Spark SQL ile doğrula.

**Yapman gerekenler:**

1. `df = spark.createDataFrame(make_orders(50_000), numPartitions=4)`.
2. `revenue` sütununu ekle (`"quantity * unit_price"`), yalnızca
   `payment == 'card'` olanları süz.
3. `groupBy("category").agg({"revenue": "sum", "order_id": "count"})`,
   `orderBy("category")`; sonucu `toPandas()` ile al.
4. Her satıra kategoriyi, sipariş sayısını ve ciroyu (iki ondalık) yazdır.
   Sütun adları `sum(revenue)` ve `count(order_id)`.
5. `df.createOrReplaceTempView("orders")`; `spark.sql` ile kartla ödenen
   sipariş sayısını bul ve rapordaki sayıların toplamına eşit olup
   olmadığını yazdır.

**Beklenen çıktı:**

```
books 7801 3296344.0
clothing 7974 9775615.22
electronics 5091 28591960.41
home 7090 7561763.12
sports 3610 6548086.31
toys 4357 3315431.27
True
```
