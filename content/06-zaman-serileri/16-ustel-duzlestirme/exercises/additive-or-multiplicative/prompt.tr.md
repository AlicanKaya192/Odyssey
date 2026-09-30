Aylık yolcu serisinde 2024'ü üç farklı Holt–Winters biçimiyle tahmin et ve
Bölüm 14'ün çıtasıyla karşılaştır.

Başlangıç kodunda `train` (2023 sonuna kadar) ve `test` (2024) hazır.

**Yapman gerekenler:**

1. Çıtayı hesapla: 2023'ün değerleri × (`2023 toplamı / 2022 toplamı`).
   Ortalama mutlak hatasını iki ondalıkla yazdır.
2. Üç model kur (`seasonal_periods=12`):
   - `"add-add"`: `trend="add"`, `seasonal="add"`
   - `"add-mul"`: `trend="add"`, `seasonal="mul"`
   - `"mul-mul"`: `trend="mul"`, `seasonal="mul"`
3. Her biri için 12 aylık tahminin ortalama mutlak hatasını (iki ondalık) ve
   yüzde hatasını (bir ondalık) `ad MAE yüzde` biçiminde alt alta yazdır.
4. En iyi modelin çıtaya göre becerisini iki ondalıkla yazdır.
5. En iyi modelin üç düzleştirme katsayısını (`smoothing_level`,
   `smoothing_trend`, `smoothing_seasonal`) iki ondalıkla liste olarak
   yazdır.
6. En iyi modelin Ağustos 2024 tahminini ve gerçek değeri tam sayıya
   yuvarlayıp aynı satıra yazdır.

**Beklenen çıktı:**

```
11.11
add-add 9.9 2.4
add-mul 8.61 2.2
mul-mul 6.53 1.7
0.41
[0.0, 0.0, 0.0]
494 480
```

Üç model de çıtayı geçiyor; serinin yapısına uyan (yüzdeyle büyüme, orantılı
mevsim) en iyisi. Katsayılarının üçü de sıfır: model, başlangıçta bulduğu
büyüme oranını ve aylık çarpanları 11 yıl boyunca hiç değiştirmeye gerek
görmemiş. Desen bu kadar kararlı olduğunda iyi bir tahmin için gereken tek
şey doğru biçimi seçmek.
