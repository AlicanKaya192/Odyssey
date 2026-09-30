Berlin'deki ekip her gün 09:00'da toplantı yapıyor; İstanbul'daki
ekip bağlanıyor. 31 Mart 2024 gecesi Berlin saatleri bir saat ileri aldı.

**Yapman gerekenler:**

1. `berlin = ZoneInfo("Europe/Berlin")` ve
   `istanbul = ZoneInfo("Europe/Istanbul")` tanımla.
2. 30 Mart 2024 09:00 ve 31 Mart 2024 09:00 Berlin toplantılarını dilimli
   `datetime` olarak kur (`tzinfo=berlin`).
3. İkisinin İstanbul'daki saatini `astimezone(istanbul)` ile bul ve
   `"%H:%M"` biçiminde alt alta yazdır.
4. Berlin'de 30 Mart 12:00 ile 31 Mart 12:00 arasında **gerçekte** kaç saat
   geçtiğini hesapla: ikisini `astimezone(timezone.utc)` ile UTC'ye çevir,
   farkın `total_seconds() / 3600` değerini yazdır.

**Beklenen çıktı:**

```
11:00
10:00
23.0
```

İstanbul'dan bakınca toplantı bir gecede bir saat öne geldi. Son satır, aynı
dilimde çıkarmanın göstermediği gerçeği söylüyor: o "bir gün" 23 saat
sürdü.
