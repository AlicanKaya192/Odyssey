Bölüm 17'deki günlük mağaza satışına dön. ARIMA'nın en kötü deneyi yıl
sonundaydı. Modele iki takvim bilgisi ver: yıllık dalga (Fourier) ve Aralık
tırmanışı.

Başlangıç kodunda `train` (3 Aralık 2024'e kadar) ve `test` (sonraki 28 gün)
hazır.

**Yapman gerekenler:**

1. `fourier(index, K)` fonksiyonunu yaz: `day = index.dayofyear.to_numpy()`;
   her `k = 1..K` için `sin{{k}}` ve `cos{{k}}` sütunları
   (`np.sin(2 * np.pi * k * day / 365.25)` ve kosinüsü); indeksi `index` olan
   bir tablo döndürsün.
2. `calendar(index)` fonksiyonunu yaz: `fourier(index, 2)` tablosuna bir `dec`
   sütunu eklesin: Aralık günlerinde `index.day / 31`, öteki günlerde 0.
3. `calendar(train.index)` tablosunun şeklini ve sütun adlarını aynı satıra
   yazdır.
4. İki model kur (ikisi de `order=(0, 1, 1)`, `seasonal_order=(0, 1, 1, 7)`):
   biri dış değişkensiz, öteki `exog=calendar(train.index)` ile.
5. İki modelin 28 günlük tahminini al (ikincisine
   `exog=calendar(test.index)` ver). Ortalama mutlak hatalarını ve
   yanlılıklarını iki ondalıkla `ad MAE yanlılık` biçiminde alt alta yazdır
   (adlar: `plain`, `calendar`).
6. `dec` sütununun katsayısını bir ondalıkla yazdır.

**Beklenen çıktı:**

```
(1068, 5) ['sin1', 'cos1', 'sin2', 'cos2', 'dec']
plain 31.34 31.07
calendar 14.35 9.5
49.4
```

Yalın model Aralık tırmanışını bilmiyor: 28 günün hepsinde düşük kalıyor
(yanlılık neredeyse MAE kadar). Takvim bilgisiyle hata yarıdan fazla azalıyor
ve yanlılık 31'den 9.5'e iniyor. `dec` katsayısı, ay sonuna doğru satışın kaç
birim yükseldiğini söylüyor. Fourier sütunlarının geleceği için hiçbir tahmin
gerekmedi: yılın günü takvimden belli.
