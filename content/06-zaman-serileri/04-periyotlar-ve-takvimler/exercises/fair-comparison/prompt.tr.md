Şubat 2024 ile Mart 2024'ü karşılaştır. Toplama bakınca bir ay, günlük
ortalamaya bakınca öteki ay önde.

**Yapman gerekenler:**

1. Dosyayı oku ve aylık toplamları hesapla (`to_period("M")`).
2. Şubat ve Mart 2024 toplamlarını aynı satıra yazdır.
3. İki ayın gün sayısını aynı satıra yazdır. Periyodun gün sayısı:
   `pd.Period("2024-02", "M").days_in_month`.
4. Her ay için toplamı gün sayısına bölüp bir ondalığa yuvarla; ikisini aynı
   satıra yazdır.
5. Günlük ortalaması daha yüksek olan ayı `February` ya da `March` olarak
   yazdır.

**Beklenen çıktı:**

```
8491 8919
29 31
292.8 287.7
February
```

Toplam Mart'ı öne koyuyor, günlük ortalama Şubat'ı. Aradaki fark satıştan
değil, Mart'ın iki gün uzun olmasından geliyor.
