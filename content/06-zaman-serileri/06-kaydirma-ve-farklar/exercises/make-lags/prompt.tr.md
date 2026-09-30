Her günün yanına dünün ve geçen haftanın satışını getir.

**Yapman gerekenler:**

1. `store_sales.csv` dosyasını tarih indeksli `s` serisi olarak oku.
2. Üç sütunlu bir tablo kur: `sales` (seri), `lag1` (`shift(1)`), `lag7`
   (`shift(7)`).
3. `lag1` ve `lag7` sütunlarındaki `NaN` sayılarını aynı satıra yazdır.
4. 9 Mart 2024 satırındaki üç değeri liste olarak yazdır (`.tolist()`).
5. Satışın `lag1` ve `lag7` ile korelasyonunu üç ondalığa yuvarlayıp aynı
   satıra yazdır.

**Beklenen çıktı:**

```
1 7
[384.0, 288.0, 372.0]
0.695 0.958
```

Bölüm 00'da aynı iki korelasyonu diziyi elle dilimleyerek bulmuştun. `shift`
aynı işi tarihleri kaybetmeden yapıyor.
