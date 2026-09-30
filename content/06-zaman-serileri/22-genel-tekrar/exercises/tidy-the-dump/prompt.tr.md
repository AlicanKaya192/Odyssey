Kiralama sisteminin ham dökümünü (`bike_raw.csv`) düzenli, boşluksuz bir günlük
seriye çevir. Tarihler `29.01.2022` biçiminde, satırlar sırasız.

**Yapman gerekenler:**

1. Dosyayı oku ve `date` sütununu `format="%d.%m.%Y"` ile tarihe çevir. Satır
   sayısını ve tamamen aynı olan (çift) satır sayısını aynı satıra yazdır.
2. Çiftleri at, tarihi indeks yap, sırala, `rentals` sütununu al ve
   `asfreq("D")` ile günlük sıklığa getir. Eksik gün sayısını ve en uzun
   boşluğun kaç gün olduğunu aynı satıra yazdır.
3. En düşük değerin gününü (`"%Y-%m-%d"`), değerini, bir hafta öncesinin ve bir
   hafta sonrasının değerini (tam sayılar) aynı satıra yazdır.
4. O günü de eksik say (`NaN` yap). Bütün eksikleri bir hafta öncesi ile bir
   hafta sonrasının ortalamasıyla doldur ve sonucu tam sayıya yuvarla.
5. 5–8 Haziran 2023 için doldurulan değerleri liste olarak yazdır.
6. Son serinin uzunluğunu, kalan eksik sayısını ve toplamını aynı satıra
   yazdır.

**Beklenen çıktı:**

```
1093 6
9 4
2024-07-16 9 600 311
[348, 491, 476, 485]
1096 0 400910
```

1093 satırlık sırasız bir dökümden 1096 günlük düzenli bir seri çıktı. 16
Temmuz'daki 9 kiralama, komşu haftaların 600 ve 311'i yanında açıkça bir
arıza: talep değil, ölçüm. Dört günlük boşluk bile dolduruldu, çünkü bir hafta
öncesi ve sonrası yerindeydi.
