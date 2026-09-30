Tarih indeksli seride aralık seç.

**Yapman gerekenler:**

1. `store_sales.csv` dosyasını tarih indeksli `s` serisi olarak oku.
2. 4–10 Mart 2024 haftasını seç; satır sayısını ve toplamını aynı satıra
   yazdır.
3. 2024'ün ilk çeyreğini (`"2024-01":"2024-03"`) seç; gün sayısını ve
   toplamını aynı satıra yazdır.
4. Aralık 2024'ün ortalama satışını bir ondalığa yuvarlayıp yazdır.
5. 2024'ün en yüksek satışlı gününü bul (`idxmax()`); tarihi
   `"%Y-%m-%d"` biçiminde ve o günün satışını aynı satıra yazdır.

**Beklenen çıktı:**

```
7 1978
91 26513
365.6
2024-12-28 503
```

Hafta için yedi gün geldi: tarih dilimi son günü de alıyor. İlk çeyrek 91
gün, çünkü 2024 artık yıl ve Şubat 29 gün.
