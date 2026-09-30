Eksik günleri olan seride "son 7 günün toplamı" iki farklı şey olabiliyor.

**Yapman gerekenler:**

1. `sales_messy.csv` dosyasını oku, sırala ve tekrarları topla → `fixed`.
2. 20 Temmuz 2024 için satır penceresiyle toplamı yazdır:
   `fixed.rolling(7).sum()`.
3. O yedi satırın kapsadığı aralığı gün olarak bul: `fixed` içinde 20
   Temmuz'dan geriye yedinci satırın tarihini bul ve 20 Temmuz ile arasındaki
   gün farkına 1 ekle. Sonucu yazdır.
4. Aynı gün için süre penceresiyle toplamı ve o pencerede kaç kayıt olduğunu
   aynı satıra yazdır: `fixed.rolling("7D").sum()` ve `.count()`.
5. Süre penceresinde 7'den az kaydı olan gün sayısını yazdır
   (`fixed.rolling("7D").count() < 7`).

**Beklenen çıktı:**

```
2092.0
10
1200.0 4.0
36
```

Satır penceresi yedi kaydı topluyor ama o kayıtlar 10 güne yayılmış. Süre
penceresi gerçekten son 7 güne bakıyor ve yalnızca dört kayıt buluyor. İkisi
de tek başına "haftalık satış" değil; ama ikincisi en azından kaç gözleme
dayandığını söylüyor.
