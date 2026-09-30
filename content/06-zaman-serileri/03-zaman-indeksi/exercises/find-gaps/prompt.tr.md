Tekrarları çözdükten sonra 358 satır kalıyor; 2024 ise 366 gün. Hangi
günler yok?

**Yapman gerekenler:**

1. Dosyayı oku, sırala ve tekrarları topla (önceki alıştırmadaki gibi).
2. İlk tarihten son tarihe tam günlük takvimi üret (`pd.date_range`,
   `freq="D"`) ve seride olmayan günleri bul (`difference`).
3. Eksik gün sayısını ve eksik tarihleri (`"%Y-%m-%d"`, liste) yazdır.
4. Art arda iki satır arasındaki **en uzun** aralığı gün olarak yazdır:
   `fixed.index.to_series().diff().max().days`.
5. Seriyi `asfreq("D")` ile tam takvime oturt; satır sayısını ve `NaN`
   sayısını aynı satıra yazdır.

**Beklenen çıktı:**

```
8
['2024-02-10', '2024-02-11', '2024-04-23', '2024-07-15', '2024-07-16', '2024-07-17', '2024-10-29', '2024-12-25']
4
366 8
```

En uzun aralık 4 gün: 14 Temmuz'dan sonraki satır 18 Temmuz. `asfreq` öncesi
bu seride "bir önceki satır" her zaman dün değildi; sonrası her gün için bir
satır var ve eksikler `NaN` olarak görünüyor.
