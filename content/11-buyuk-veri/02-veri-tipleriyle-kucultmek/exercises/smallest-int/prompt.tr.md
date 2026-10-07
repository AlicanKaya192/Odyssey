100 000 siparişlik tabloda üç tam sayı sütunu için en küçük güvenli türü
bul.

**Yapman gerekenler:**

1. `make_orders(100_000)` ile `df` tablosunu kur.
2. `quantity`, `customer_id` ve `order_id` sütunlarını bir döngüyle gez.
3. Her sütun için bir satıra şunları yazdır: sütunun adı, en küçük değeri,
   en büyük değeri ve `pd.to_numeric(..., downcast="integer")` sonucunun
   türü (`dtype`).

**Beklenen çıktı:**

```
quantity 1 5 int8
customer_id 1 24999 int16
order_id 1 100000 int32
```

Üç sütun, üç farklı tür: `customer_id` bu tabloda 25 000'in altında
kaldığı için `int16`'ya sığıyor.
