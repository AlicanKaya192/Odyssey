Bir sipariş 27 Şubat 2024'te verilmiş, 4 Mart 2024'te teslim edilmiş.

**Yapman gerekenler:**

1. İki tarihi `date` olarak kur.
2. Aradaki gün sayısını yazdır (`(teslim - siparis).days`).
3. Teslim gününün adını yazdır (`strftime("%A")`).
4. Aynı iki günü 2023 yılı için kurup aradaki gün sayısını yazdır.

**Beklenen çıktı:**

```
6
Monday
5
```

Aynı iki tarih iki yılda farklı sonuç veriyor: 2024 artık yıl ve araya 29
Şubat giriyor. Elle hesaplarken en kolay kaçırılan şey bu.
