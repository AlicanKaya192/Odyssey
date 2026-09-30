`cafe_daily.csv` bir iş merkezindeki kafenin üç yıllık günlük satışı.
Sütunlar: `date`, `sales`, `temp_c` (günün ortalama sıcaklığı), `promo`
(kampanya günü: 1), `holiday` (resmi tatil: 1).

**Yapman gerekenler:**

1. Dosyayı tarih indeksli oku ve `asfreq("D")` uygula. Tablonun şeklini
   yazdır.
2. Kampanya ve tatil günlerinin sayısını aynı satıra yazdır.
3. Kampanya günlerinin hangi günlere denk geldiğini yazdır: `promo == 1` olan
   satırların `dayofweek` değerlerinin sıralı, tekrarsız listesi.
4. Ortalama satışı üç grup için bir ondalıkla aynı satıra yazdır: kampanya
   günleri, tatil günleri, öteki günler (ikisi de 0).
5. Kaba kampanya etkisini yazdır: kampanya günlerinin ortalaması eksi
   `promo == 0` olan günlerin ortalaması (bir ondalık).
6. Satış ile sıcaklığın korelasyonunu iki ondalıkla yazdır.

**Beklenen çıktı:**

```
(1096, 4)
84 41
[3, 4, 5]
284.0 166.7 229.6
57.0
0.62
```

Kampanyalar hep perşembe, cuma ve cumartesi (3, 4, 5). Bu yüzden 5. satırdaki
"kaba etki" güvenilir değil: kampanya günlerini bütün günlerle
karşılaştırıyor, oysa o üç günün satışı zaten farklı. Sıcaklıkla korelasyon
da yüksek: yazın kalabalık bir kafe.
