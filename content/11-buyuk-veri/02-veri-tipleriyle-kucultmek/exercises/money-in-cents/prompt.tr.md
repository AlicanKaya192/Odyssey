Bir milyon siparişin fiyat toplamını üç farklı saklama biçimiyle hesapla
ve sapmaları karşılaştır.

**Yapman gerekenler:**

1. `make_orders(1_000_000)` ile tabloyu kur; `prices = df["unit_price"]`.
2. Gerçek toplam: `prices.sum()`.
3. `float32` toplamı: fiyatları `float32` yap ve **`float32` içinde** topla
   (`.sum()`), sonucu `float(...)` ile sayıya çevir.
4. Kuruş toplamı: fiyatları kuruşa çevir
   (`(prices * 100).round().astype("int64")`), topla ve 100'e böl.
5. Üç toplamı iki ondalığa yuvarlayıp ayrı satırlara yazdır.
6. Son satıra `float32` toplamının gerçek toplamdan farkını ve kuruş
   toplamının gerçek toplamdan farkını, ikisi de iki ondalık, aynı satıra
   yazdır.

**Beklenen çıktı:**

```
736869041.37
736869056.0
736869041.37
14.63 0.0
```

Kuruş toplamı gerçek toplamla kuruşu kuruşuna aynı; `float32` toplamı ise
14,63 TL saptı.
