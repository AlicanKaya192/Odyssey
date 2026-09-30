`sales_messy.csv` aynı mağazanın 2024 kayıtları, ama satırlar karışık
sırada gelmiş. Sıralamadan tarih aralığı seçilemiyor.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli `messy` serisi olarak oku.
2. İndeksin sıralı olup olmadığını yazdır (`is_monotonic_increasing`).
3. `sort_index()` ile sırala ve aynı kontrolü tekrar yazdır.
4. İlk ve son tarihi `"%Y-%m-%d"` biçiminde aynı satıra yazdır.
5. 4–10 Mart haftasını seç; satır sayısını ve toplamını aynı satıra yazdır.

**Beklenen çıktı:**

```
False
True
2024-01-01 2024-12-31
8 1978
```

Son satıra dikkat: yedi günlük hafta için **sekiz** satır geldi. Toplam doğru
(temiz dosyadaki 1978), ama bir gün iki kez yazılmış. Bir sonraki alıştırmada
onu çözeceksin.
