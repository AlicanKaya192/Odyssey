Üç aykırı günü (14 Mart, 20 Haziran, 8 Ekim) onar: eksik say, bir hafta
öncesi ile sonrasının ortalamasıyla doldur. Özgün veriyi koru ve dokunduğun
günleri işaretle.

**Yapman gerekenler:**

1. `clean = visits.astype(float).copy()` al ve üç günü `NaN` yap.
2. Boşlukları bir hafta öncesi ile sonrasının ortalamasıyla doldur
   (`pd.concat([clean.shift(7), clean.shift(-7)], axis=1).mean(axis=1)`).
3. Üç günün yeni değerlerini liste olarak yazdır.
4. Bir tablo kur: `visits` (özgün), `clean` (düzeltilmiş) ve `repaired`
   (dokunulan günlerde `True`). Satır sayısını ve `repaired` toplamını aynı
   satıra yazdır.
5. Standart sapmayı düzeltmeden önce ve sonra bir ondalığa yuvarlayıp aynı
   satıra yazdır.
6. Perşembe günlerinin (`dayofweek == 3`) ortalamasını düzeltmeden önce ve
   sonra bir ondalığa yuvarlayıp aynı satıra yazdır.
7. Kampanyaların toplam etkisini yazdır: iki kampanya gününde özgün değer ile
   düzeltilmiş değer arasındaki farkların toplamı (tam sayı).

**Beklenen çıktı:**

```
[4116.0, 4120.5, 5226.5]
366 3
914.2 805.6
4621.3 4423.5
10285
```

Satır sayısı değişmedi: hiçbir gün silinmedi, yalnızca üç değer değişti.
Standart sapma 108 birim düştü ve perşembe ortalaması 200 birim geriledi:
haftalık desen artık iki kampanya tarafından çarpıtılmıyor. Özgün sütunu
sakladığın için son soruyu da cevaplayabildin: iki kampanya yaklaşık 10 bin
ek ziyaret getirdi.
