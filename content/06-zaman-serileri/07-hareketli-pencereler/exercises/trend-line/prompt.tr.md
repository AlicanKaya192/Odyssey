365 günlük pencere hem haftalık hem yıllık deseni bastırıyor; geriye trend
kalıyor.

**Yapman gerekenler:**

1. Dosyayı oku ve 365 günlük hareketli ortalamayı hesapla.
2. Baştaki `NaN` sayısını yazdır.
3. 31 Aralık 2022, 2023 ve 2024'teki değerleri bir ondalığa yuvarlayıp aynı
   satıra yazdır.
4. Aynı üç yılın ortalamalarını (`s.resample("YE").mean()`) bir ondalığa
   yuvarlayıp liste olarak yazdır.
5. Trendin bir yılda ne kadar yükseldiğini bul: 31 Aralık 2024'teki değerden
   31 Aralık 2023'teki değeri çıkar, bir ondalığa yuvarla.

**Beklenen çıktı:**

```
364
225.5 260.4 294.1
[225.5, 260.4, 294.0]
33.7
```

Yıl sonlarındaki hareketli ortalama, o yılın ortalamasıyla neredeyse aynı
(2024 artık yıl olduğu için pencere yılın 366 gününden 365'ini kapsıyor).
Bedeli ilk satırda: bir yıla yakın veri trend hesabına gidiyor.
