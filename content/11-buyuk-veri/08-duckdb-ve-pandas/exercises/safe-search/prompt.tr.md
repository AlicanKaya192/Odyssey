Şehir ve en az adet alan, parametreli bir arama fonksiyonu yaz.

**Yapman gerekenler:**

1. Başlangıç kodu 100 000 siparişi `orders.parquet` olarak yazıyor.
2. `count_orders(city, min_quantity)` fonksiyonunu yaz: `city` şehrinde,
   adedi `min_quantity` ya da daha fazla olan siparişlerin sayısını
   döndürsün. İki değeri de `?` ile ver:
   `duckdb.execute(sorgu, [city, min_quantity]).fetchone()[0]`.
3. Şunları ayrı satırlara yazdır:
   - `count_orders("Izmir", 3)`
   - `count_orders("Bursa", 5)`
   - `count_orders("Izmir' OR '1'='1", 1)`

**Beklenen çıktı:**

```
4367
994
0
```

Son satır 0: kötü niyetli metin sorgunun parçası olamadı.
