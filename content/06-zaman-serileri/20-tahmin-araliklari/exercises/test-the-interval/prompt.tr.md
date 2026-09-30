Modelin "%95" dediği aralık gerçekten %95 tutuyor mu? Bölüm 15'in
düzeneğiyle ölç: 13 başlangıç, 28 günlük ufuk. (Birkaç saniye sürer.)

Başlangıç kodunda `cuts` hazır.

**Yapman gerekenler:**

1. Her kesimde: eğitim `s.loc[:cut]`, test sonraki 28 gün.
   `ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 7))` kur,
   `get_forecast(28)` al ve %95 aralığı hesapla.
2. Her deney için gerçek değerlerin aralığın içinde olup olmadığını (28
   doğru/yanlış) ve aralığın ortalama genişliğini sakla.
3. Bütün deneylerin toplam kapsamasını üç ondalıkla yazdır.
4. Deney deney kapsamayı iki ondalıkla liste olarak yazdır.
5. Kapsaması 0.8'in altında kalan deneylerin kesim günlerini `"%Y-%m-%d"`
   listesi olarak yazdır.
6. Bu deneyler çıkarılınca kalanların kapsamasını üç ondalıkla ve ortalama
   aralık genişliğini bir ondalıkla aynı satıra yazdır.

**Beklenen çıktı:**

```
0.874
[0.0, 0.96, 1.0, 1.0, 0.96, 1.0, 1.0, 1.0, 0.93, 1.0, 1.0, 0.96, 0.54]
['2024-01-02', '2024-12-03']
0.984 68.5
```

"%95" aralık 13 deneyde %87 tutuyor: fazla dar. Ama sorun her yerde değil:
iki deney (yılın başı ve sonu) çöküyor, öbür on bir deneyde kapsama kusursuza
yakın. Aralık, modelin bildiği belirsizliği ölçüyor; model yıl dönümündeki
hareketi bilmediği için aralığı da bilmiyor. Çare daha geniş bir aralık değil,
eksik bilgi (Bölüm 18'deki takvim değişkenleri).
