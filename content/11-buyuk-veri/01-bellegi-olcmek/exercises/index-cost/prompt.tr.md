Aynı tabloyu üç farklı indeksle kur ve indeksin kapladığı yeri karşılaştır.

**Yapman gerekenler:**

1. `make_orders(50_000)` ile `df` tablosunu kur (dosya yok).
2. Üç tablo hazırla: `df` (varsayılan indeks), `df.set_index("order_id")`,
   `df.set_index("customer_id")`.
3. Her biri için bir satıra indeksin türünün adını
   (`type(t.index).__name__`) ve indeksin baytını
   (`t.memory_usage(deep=True)["Index"]`) yazdır. Üç tabloyu bir listeye
   koyup döngüyle gez.
4. Son satıra `customer_id` indeksli tablonun toplam belleğinin (indeks
   dahil) MB olarak değerini bir ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
RangeIndex 132
RangeIndex 132
Index 400000
4.8
```

`order_id` düzenli arttığı için yine `RangeIndex` oldu.
