Günlük satışı aylara topla.

**Yapman gerekenler:**

1. `store_sales.csv` dosyasını tarih indeksli `s` serisi olarak oku.
2. Her günü ait olduğu aya atayıp topla:
   `s.groupby(s.index.to_period("M")).sum()`.
3. Kaç ay olduğunu yazdır.
4. Mart 2024'ün toplamını yazdır.
5. En yüksek toplamlı ayı ve toplamını aynı satıra yazdır (`idxmax()`).

**Beklenen çıktı:**

```
36
8919
2024-12 11335
```

Üç yıl 36 aya indi. İndeks artık günler değil, aylar: bir `PeriodIndex`.
