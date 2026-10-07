Her müşterinin ilk siparişini `QUALIFY` ile bul.

**Yapman gerekenler:**

1. Başlangıç kodu 100 000 siparişi `orders.parquet` olarak yazıyor.
2. `QUALIFY row_number() OVER (PARTITION BY customer_id ORDER BY
   order_time) = 1` ile her müşterinin ilk siparişini seçen sorguyu
   `first` adlı bir değişkene koy.
3. `first` üstünde üç şeyi bul ve yazdır:
   - kaç müşteri olduğu (`count(*)`),
   - ilk siparişi Ocak ayında olan müşteri sayısı
     (`month(order_time) = 1`),
   - müşteri numarası en küçük üç müşterinin `customer_id` ve `order_id`
     değerleri (her biri ayrı satırda).

**Beklenen çıktı:**

```
24512
7049
1 20221
2 61138
3 3294
```
