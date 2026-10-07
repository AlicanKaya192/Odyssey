Bu kez sınıra hiç çarpma: istekleri aralıklı gönder.

**Yapman gerekenler:**

1. `/limited`'e 6 istek gönder; her istekten sonra `GAP` kadar bekle.
2. Gelen kodları `codes` listesine topla ve yazdır.
3. Hiç 429 gelmediyse `no 429` yazdır.

`GAP` değerini sen seç: saniyede 3 hak var; aralık `1 / 3` saniyeden biraz
büyük olmalı.

**Beklenen çıktı:**

```
[200, 200, 200, 200, 200, 200]
no 429
```
