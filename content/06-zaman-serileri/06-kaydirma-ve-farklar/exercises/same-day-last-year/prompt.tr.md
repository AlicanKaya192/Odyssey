9 Mart 2024'ün satışını geçen yılla karşılaştır: önce 365, sonra 364 gün
geriye giderek.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli `s` serisi olarak oku.
2. `day = pd.Timestamp("2024-03-09")` için üç günün adını aynı satıra yazdır:
   günün kendisi, 365 gün öncesi, 364 gün öncesi (`day_name()`).
3. O gün için iki yıllık büyümeyi yüzde olarak hesapla ve bir ondalığa
   yuvarlayıp aynı satıra yazdır: `s.shift(365)` ile ve `s.shift(364)` ile.
4. Aynı iki büyüme oranını 2024'ün **bütün günleri** için hesapla; ikisinin
   standart sapmasını bir ondalığa yuvarlayıp aynı satıra yazdır.

**Beklenen çıktı:**

```
Saturday Friday Saturday
44.9 18.9
18.7 7.2
```

365 gün geriye gitmek cumartesiyi cumayla karşılaştırıyor ve büyümeyi iki
katından fazla şişiriyor. Son satırda 365'in yayılımı çok daha geniş: o
oynamanın çoğu büyüme değil, haftanın günlerinin karışması.
