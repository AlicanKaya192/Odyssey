`head` ile rastgele örneklemin yılı ne kadar kapsadığını karşılaştır.

**Yapman gerekenler:**

1. `orders = make_orders(200_000)`; `order_time`'ı tarihe çevir.
2. İki örneklem hazırla: `orders.head(5_000)` ve
   `orders.sample(n=5_000, random_state=0)`.
3. Her biri için bir satıra adını (`head` / `random`), kapsadığı farklı ay
   sayısını ve en erken ile en geç tarihi (`.date()`) yazdır.
4. Her biri için kapsadığı farklı gün sayısını
   (`order_time.dt.date.nunique()`) bir satıra, önce `head`, sonra
   `random` olarak yazdır.

**Beklenen çıktı:**

```
head 1 2024-01-01 2024-01-10
random 12 2024-01-01 2024-12-31
head 10
random 366
```

`head` yalnızca Ocak'ın ilk günlerini gördü.
