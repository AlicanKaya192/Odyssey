Her satır grubunun hangi tarihleri kapsadığını istatistiklerden oku.

**Yapman gerekenler:**

1. Başlangıç kodu 200 000 siparişi 40 000 satırlık gruplarla yazıyor.
2. `order_time` sütununun sırasını `schema_arrow.names.index(...)` ile
   bul.
3. Her satır grubu için bir satıra grubun numarasını, `order_time`
   istatistiğinin en küçük ve en büyük değerinin **tarihini** (`.date()`)
   yazdır.

**Beklenen çıktı:**

```
0 2024-01-01 2024-03-14
1 2024-03-14 2024-05-26
2 2024-05-26 2024-08-07
3 2024-08-07 2024-10-20
4 2024-10-20 2024-12-31
```

Gruplar yılı çakışmadan beşe bölüyor; zamana göre süzerken her biri tek
başına atlanabilir.
